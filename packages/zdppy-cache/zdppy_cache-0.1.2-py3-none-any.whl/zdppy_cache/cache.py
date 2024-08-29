from .core import Disk
import codecs
import contextlib as cl
import errno
import functools as ft
import io
import json
import os
import os.path as op
import pickle
import pickletools
import sqlite3
import struct
import tempfile
import threading
import time
import warnings
import zlib

from .core import (
    ENOVAL, DBNAME, DEFAULT_SETTINGS,
    METADATA, EVICTION_POLICY,
)


class Cache:
    """Disk and file backed cache."""

    def __init__(self, directory=None, timeout=60, disk=Disk, **settings):
        """Initialize cache instance.

        :param str directory: cache directory
        :param float timeout: SQLite connection timeout
        :param disk: Disk type or subclass for serialization
        :param settings: any of DEFAULT_SETTINGS

        """
        try:
            assert issubclass(disk, Disk)
        except (TypeError, AssertionError):
            raise ValueError('disk must subclass zdppy_cache.Disk') from None

        if directory is None:
            directory = tempfile.mkdtemp(prefix='zdppy_cache-')
        directory = str(directory)
        directory = op.expanduser(directory)
        directory = op.expandvars(directory)

        self._directory = directory
        self._timeout = 0  # Manually handle retries during initialization.
        self._local = threading.local()
        self._txn_id = None

        if not op.isdir(directory):
            try:
                os.makedirs(directory, 0o755)
            except OSError as error:
                if error.errno != errno.EEXIST:
                    raise EnvironmentError(
                        error.errno,
                        'Cache directory "%s" does not exist'
                        ' and could not be created' % self._directory,
                    ) from None

        sql = self._sql_retry

        # Setup Settings table.

        try:
            current_settings = dict(
                sql('SELECT key, value FROM Settings').fetchall()
            )
        except sqlite3.OperationalError:
            current_settings = {}

        sets = DEFAULT_SETTINGS.copy()
        sets.update(current_settings)
        sets.update(settings)

        for key in METADATA:
            sets.pop(key, None)

        # Chance to set pragmas before any tables are created.

        for key, value in sorted(sets.items()):
            if key.startswith('sqlite_'):
                self.reset(key, value, update=False)

        sql(
            'CREATE TABLE IF NOT EXISTS Settings ('
            ' key TEXT NOT NULL UNIQUE,'
            ' value)'
        )

        # Setup Disk object (must happen after settings initialized).

        kwargs = {
            key[5:]: value
            for key, value in sets.items()
            if key.startswith('disk_')
        }
        self._disk = disk(directory, **kwargs)

        # Set cached attributes: updates settings and sets pragmas.

        for key, value in sets.items():
            query = 'INSERT OR REPLACE INTO Settings VALUES (?, ?)'
            sql(query, (key, value))
            self.reset(key, value)

        for key, value in METADATA.items():
            query = 'INSERT OR IGNORE INTO Settings VALUES (?, ?)'
            sql(query, (key, value))
            self.reset(key)

        ((self._page_size,),) = sql('PRAGMA page_size').fetchall()

        # Setup Cache table.

        sql(
            'CREATE TABLE IF NOT EXISTS Cache ('
            ' rowid INTEGER PRIMARY KEY,'
            ' key BLOB,'
            ' raw INTEGER,'
            ' store_time REAL,'
            ' expire_time REAL,'
            ' access_time REAL,'
            ' access_count INTEGER DEFAULT 0,'
            ' tag BLOB,'
            ' size INTEGER DEFAULT 0,'
            ' mode INTEGER DEFAULT 0,'
            ' filename TEXT,'
            ' value BLOB)'
        )

        sql(
            'CREATE UNIQUE INDEX IF NOT EXISTS Cache_key_raw ON'
            ' Cache(key, raw)'
        )

        sql(
            'CREATE INDEX IF NOT EXISTS Cache_expire_time ON'
            ' Cache (expire_time)'
        )

        query = EVICTION_POLICY[self.eviction_policy]['init']

        if query is not None:
            sql(query)

        # Use triggers to keep Metadata updated.

        sql(
            'CREATE TRIGGER IF NOT EXISTS Settings_count_insert'
            ' AFTER INSERT ON Cache FOR EACH ROW BEGIN'
            ' UPDATE Settings SET value = value + 1'
            ' WHERE key = "count"; END'
        )

        sql(
            'CREATE TRIGGER IF NOT EXISTS Settings_count_delete'
            ' AFTER DELETE ON Cache FOR EACH ROW BEGIN'
            ' UPDATE Settings SET value = value - 1'
            ' WHERE key = "count"; END'
        )

        sql(
            'CREATE TRIGGER IF NOT EXISTS Settings_size_insert'
            ' AFTER INSERT ON Cache FOR EACH ROW BEGIN'
            ' UPDATE Settings SET value = value + NEW.size'
            ' WHERE key = "size"; END'
        )

        sql(
            'CREATE TRIGGER IF NOT EXISTS Settings_size_update'
            ' AFTER UPDATE ON Cache FOR EACH ROW BEGIN'
            ' UPDATE Settings'
            ' SET value = value + NEW.size - OLD.size'
            ' WHERE key = "size"; END'
        )

        sql(
            'CREATE TRIGGER IF NOT EXISTS Settings_size_delete'
            ' AFTER DELETE ON Cache FOR EACH ROW BEGIN'
            ' UPDATE Settings SET value = value - OLD.size'
            ' WHERE key = "size"; END'
        )

        # Create tag index if requested.

        if self.tag_index:  # pylint: disable=no-member
            self.create_tag_index()
        else:
            self.drop_tag_index()

        # Close and re-open database connection with given timeout.

        self.close()
        self._timeout = timeout
        self._sql  # pylint: disable=pointless-statement

    @property
    def directory(self):
        """Cache directory."""
        return self._directory

    @property
    def timeout(self):
        """SQLite connection timeout value in seconds."""
        return self._timeout

    @property
    def disk(self):
        """Disk used for serialization."""
        return self._disk

    @property
    def _con(self):
        # Check process ID to support process forking. If the process
        # ID changes, close the connection and update the process ID.

        local_pid = getattr(self._local, 'pid', None)
        pid = os.getpid()

        if local_pid != pid:
            self.close()
            self._local.pid = pid

        con = getattr(self._local, 'con', None)

        if con is None:
            con = self._local.con = sqlite3.connect(
                op.join(self._directory, DBNAME),
                timeout=self._timeout,
                isolation_level=None,
            )

            # Some SQLite pragmas work on a per-connection basis so
            # query the Settings table and reset the pragmas. The
            # Settings table may not exist so catch and ignore the
            # OperationalError that may occur.

            try:
                select = 'SELECT key, value FROM Settings'
                settings = con.execute(select).fetchall()
            except sqlite3.OperationalError:
                pass
            else:
                for key, value in settings:
                    if key.startswith('sqlite_'):
                        self.reset(key, value, update=False)

        return con

    @property
    def _sql(self):
        return self._con.execute

    @property
    def _sql_retry(self):
        sql = self._sql

        # 2018-11-01 GrantJ - Some SQLite builds/versions handle
        # the SQLITE_BUSY return value and connection parameter
        # "timeout" differently. For a more reliable duration,
        # manually retry the statement for 60 seconds. Only used
        # by statements which modify the database and do not use
        # a transaction (like those in ``__init__`` or ``reset``).
        # See Issue #85 for and tests/issue_85.py for more details.

        def _execute_with_retry(statement, *args, **kwargs):
            start = time.time()
            while True:
                try:
                    return sql(statement, *args, **kwargs)
                except sqlite3.OperationalError as exc:
                    if str(exc) != 'database is locked':
                        raise
                    diff = time.time() - start
                    if diff > 60:
                        raise
                    time.sleep(0.001)

        return _execute_with_retry

    @cl.contextmanager
    def transact(self, retry=False):
        """Context manager to perform a transaction by locking the cache.

        While the cache is locked, no other write operation is permitted.
        Transactions should therefore be as short as possible. Read and write
        operations performed in a transaction are atomic. Read operations may
        occur concurrent to a transaction.

        Transactions may be nested and may not be shared between threads.

        Raises :exc:`Timeout` error when database timeout occurs and `retry` is
        `False` (default).

        >>> cache = Cache()
        >>> with cache.transact():  # Atomically increment two keys.
        ...     _ = cache.incr('total', 123.4)
        ...     _ = cache.incr('count', 1)
        >>> with cache.transact():  # Atomically calculate average.
        ...     average = cache['total'] / cache['count']
        >>> average
        123.4

        :param bool retry: retry if database timeout occurs (default False)
        :return: context manager for use in `with` statement
        :raises Timeout: if database timeout occurs

        """
        with self._transact(retry=retry):
            yield

    @cl.contextmanager
    def _transact(self, retry=False, filename=None):
        sql = self._sql
        filenames = []
        _disk_remove = self._disk.remove
        tid = threading.get_ident()
        txn_id = self._txn_id

        if tid == txn_id:
            begin = False
        else:
            while True:
                try:
                    sql('BEGIN IMMEDIATE')
                    begin = True
                    self._txn_id = tid
                    break
                except sqlite3.OperationalError:
                    if retry:
                        continue
                    if filename is not None:
                        _disk_remove(filename)
                    raise Timeout from None

        try:
            yield sql, filenames.append
        except BaseException:
            if begin:
                assert self._txn_id == tid
                self._txn_id = None
                sql('ROLLBACK')
            raise
        else:
            if begin:
                assert self._txn_id == tid
                self._txn_id = None
                sql('COMMIT')
            for name in filenames:
                if name is not None:
                    _disk_remove(name)

    def set(
            self,
            key,
            value,
            expire=180,
            read=False,
            tag=None,
            retry=False,
    ):
        """
        设置key的缓存为value，类似于存储了一个字典的键值对
        当read为True时，value应该是一个类似文件的对象，以二进制模式打开以供读取。
        当数据库超时并且retry为False(默认)时引发Timeout错误。

        :param key: 键
        :param value: 值
        :param float expire: 超时时间，默认180秒，也就是3分钟。浮点数类型，单位是秒。
        :param bool read: 是否读取二进制文件，默认False
        :param str tag: 类似于给key进行分组，打标签
        :param bool retry: 是否重试，默认False
        :return: 成功返回True
        :raises Timeout: 超时抛出异常

        """
        # 记录开始时间
        now = time.time()
        # 存储key
        db_key, raw = self._disk.put(key)
        # 计算超时时间
        expire_time = None if expire is None else now + expire
        # 进行存储
        size, mode, filename, db_value = self._disk.store(value, read, key=key)
        # 对存储的结果，进行封装，是一个元组
        columns = (expire_time, tag, size, mode, filename, db_value)

        # The order of SELECT, UPDATE, and INSERT is important below.
        # 使用示例：
        # value = cache.get(key)
        # if value is None:
        #     value = expensive_calculation()
        #     cache.set(key, value)
        #
        # Cache.get 不清理过期的键以避免查找期间的写操作。
        # 因此，常用/过期(used/expired)的键将保留在缓存中，使UPDATE成为首选路径。
        # 另一种方法是假设键不存在，首先尝试INSERT，然后处理由于违反UNIQUE约束而发生的IntegrityError。
        # 基于常见的缓存使用模式，这种乐观的方法被拒绝了。
        # INSERT OR REPLACE也就是UPSERT没有被使用，因为旧的文件名可能需要清理。

        with self._transact(retry, filename) as (sql, cleanup):
            # 执行SQL，获取结果
            rows = sql(
                'SELECT rowid, filename FROM Cache'
                ' WHERE key = ? AND raw = ?',
                (db_key, raw),
            ).fetchall()

            if rows:
                # 如果找到了，清理旧的数据，再执行更新
                ((rowid, old_filename),) = rows
                cleanup(old_filename)
                self._row_update(rowid, now, columns)
            else:
                # 如果没有找到,直接写入
                self._row_insert(db_key, raw, now, columns)

            # 计算是否超过缓存限制
            # self._cull(now, sql, cleanup)
            self.resize()

            # 成功了
            return True

    def __setitem__(self, key, value):
        """Set corresponding `value` for `key` in cache.

        :param key: key for item
        :param value: value for item
        :return: corresponding value
        :raises KeyError: if key is not found

        """
        self.set(key, value, retry=True)

    def _row_update(self, rowid, now, columns):
        sql = self._sql
        expire_time, tag, size, mode, filename, value = columns
        sql(
            'UPDATE Cache SET'
            ' store_time = ?,'
            ' expire_time = ?,'
            ' access_time = ?,'
            ' access_count = ?,'
            ' tag = ?,'
            ' size = ?,'
            ' mode = ?,'
            ' filename = ?,'
            ' value = ?'
            ' WHERE rowid = ?',
            (
                now,  # store_time
                expire_time,
                now,  # access_time
                0,  # access_count
                tag,
                size,
                mode,
                filename,
                value,
                rowid,
            ),
        )

    def _row_insert(self, key, raw, now, columns):
        sql = self._sql
        expire_time, tag, size, mode, filename, value = columns
        sql(
            'INSERT INTO Cache('
            ' key, raw, store_time, expire_time, access_time,'
            ' access_count, tag, size, mode, filename, value'
            ') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (
                key,
                raw,
                now,  # store_time
                expire_time,
                now,  # access_time
                0,  # access_count
                tag,
                size,
                mode,
                filename,
                value,
            ),
        )

    def resize(self, need_over_size=True, limit=1000):
        """
        清理缓存，会删除除了最近1000条已过期的缓存以外的其他所有缓存
        """
        if need_over_size:
            if self.volume() < self.size_limit:
                return
        with self._transact(False, self._directory) as (sql, cleanup):
            child_sql = "SELECT rowid FROM Cache ORDER BY expire_time DESC LIMIT ?"
            delete_sql = f'DELETE FROM Cache WHERE rowid NOT IN ({child_sql})'
            sql(delete_sql, (limit,))
            cleanup(self._directory)

    def _cull(self, now, sql, cleanup, limit=None):
        """
        这个方法是用来清空过期缓存的，无论是否超过限制
        :param now: 当前时间的秒值，浮点数
        :param sql: 执行清除的SQL语句
        :param cleanup: 要清除的文件夹（缓存对象）
        :param limit: 限制多少
        """
        cull_limit = self.cull_limit if limit is None else limit
        if cull_limit == 0:
            return

        # 查询已经过期的key
        select_expired_template = (
            'SELECT %s FROM Cache'
            ' WHERE expire_time IS NOT NULL AND expire_time < ?'
            ' ORDER BY expire_time LIMIT ?'
        )
        select_expired = select_expired_template % 'filename'
        rows = sql(select_expired, (now, cull_limit)).fetchall()

        if rows:
            # 如果查询到了就删除
            delete_expired = 'DELETE FROM Cache WHERE rowid IN (%s)' % (
                    select_expired_template % 'rowid'
            )
            sql(delete_expired, (now, cull_limit))
            for (filename,) in rows:
                cleanup(filename)

            # 重新计算需要清理的条数
            cull_limit -= len(rows)
            if cull_limit == 0:
                return

        # 根据policy执行删除
        # least-recently-stored
        select_policy = EVICTION_POLICY[self.eviction_policy]['cull']
        # 默认是：SELECT {fields} FROM Cache ORDER BY store_time LIMIT ?
        if select_policy is None or self.volume() < self.size_limit:
            return
        select_filename = select_policy.format(fields='filename', now=now)
        rows = sql(select_filename, (cull_limit,)).fetchall()
        if rows:
            delete = 'DELETE FROM Cache WHERE rowid IN (%s)' % (
                select_policy.format(fields='rowid', now=now)
            )
            sql(delete, (cull_limit,))

            for (filename,) in rows:
                cleanup(filename)

    def touch(self, key, expire=None, retry=False):
        """Touch `key` in cache and update `expire` time.

        Raises :exc:`Timeout` error when database timeout occurs and `retry` is
        `False` (default).

        :param key: key for item
        :param float expire: seconds until item expires
            (default None, no expiry)
        :param bool retry: retry if database timeout occurs (default False)
        :return: True if key was touched
        :raises Timeout: if database timeout occurs

        """
        now = time.time()
        db_key, raw = self._disk.put(key)
        expire_time = None if expire is None else now + expire

        with self._transact(retry) as (sql, _):
            rows = sql(
                'SELECT rowid, expire_time FROM Cache'
                ' WHERE key = ? AND raw = ?',
                (db_key, raw),
            ).fetchall()

            if rows:
                ((rowid, old_expire_time),) = rows

                if old_expire_time is None or old_expire_time > now:
                    sql(
                        'UPDATE Cache SET expire_time = ? WHERE rowid = ?',
                        (expire_time, rowid),
                    )
                    return True

        return False

    def add(self, key, value, expire=None, read=False, tag=None, retry=False):
        """Add `key` and `value` item to cache.

        Similar to `set`, but only add to cache if key not present.

        Operation is atomic. Only one concurrent add operation for a given key
        will succeed.

        When `read` is `True`, `value` should be a file-like object opened
        for reading in binary mode.

        Raises :exc:`Timeout` error when database timeout occurs and `retry` is
        `False` (default).

        :param key: key for item
        :param value: value for item
        :param float expire: seconds until the key expires
            (default None, no expiry)
        :param bool read: read value as bytes from file (default False)
        :param str tag: text to associate with key (default None)
        :param bool retry: retry if database timeout occurs (default False)
        :return: True if item was added
        :raises Timeout: if database timeout occurs

        """
        now = time.time()
        db_key, raw = self._disk.put(key)
        expire_time = None if expire is None else now + expire
        size, mode, filename, db_value = self._disk.store(value, read, key=key)
        columns = (expire_time, tag, size, mode, filename, db_value)

        with self._transact(retry, filename) as (sql, cleanup):
            rows = sql(
                'SELECT rowid, filename, expire_time FROM Cache'
                ' WHERE key = ? AND raw = ?',
                (db_key, raw),
            ).fetchall()

            if rows:
                ((rowid, old_filename, old_expire_time),) = rows

                if old_expire_time is None or old_expire_time > now:
                    cleanup(filename)
                    return False

                cleanup(old_filename)
                self._row_update(rowid, now, columns)
            else:
                self._row_insert(db_key, raw, now, columns)

            self._cull(now, sql, cleanup)

            return True

    def incr(self, key, delta=1, default=0, retry=False):
        """Increment value by delta for item with key.

        If key is missing and default is None then raise KeyError. Else if key
        is missing and default is not None then use default for value.

        Operation is atomic. All concurrent increment operations will be
        counted individually.

        Assumes value may be stored in a SQLite column. Most builds that target
        machines with 64-bit pointer widths will support 64-bit signed
        integers.

        Raises :exc:`Timeout` error when database timeout occurs and `retry` is
        `False` (default).

        :param key: key for item
        :param int delta: amount to increment (default 1)
        :param int default: value if key is missing (default 0)
        :param bool retry: retry if database timeout occurs (default False)
        :return: new value for item
        :raises KeyError: if key is not found and default is None
        :raises Timeout: if database timeout occurs

        """
        now = time.time()
        db_key, raw = self._disk.put(key)
        select = (
            'SELECT rowid, expire_time, filename, value FROM Cache'
            ' WHERE key = ? AND raw = ?'
        )

        with self._transact(retry) as (sql, cleanup):
            rows = sql(select, (db_key, raw)).fetchall()

            if not rows:
                if default is None:
                    raise KeyError(key)

                value = default + delta
                columns = (None, None) + self._disk.store(
                    value, False, key=key
                )
                self._row_insert(db_key, raw, now, columns)
                self._cull(now, sql, cleanup)
                return value

            ((rowid, expire_time, filename, value),) = rows

            if expire_time is not None and expire_time < now:
                if default is None:
                    raise KeyError(key)

                value = default + delta
                columns = (None, None) + self._disk.store(
                    value, False, key=key
                )
                self._row_update(rowid, now, columns)
                self._cull(now, sql, cleanup)
                cleanup(filename)
                return value

            value += delta

            columns = 'store_time = ?, value = ?'
            update_column = EVICTION_POLICY[self.eviction_policy]['get']

            if update_column is not None:
                columns += ', ' + update_column.format(now=now)

            update = 'UPDATE Cache SET %s WHERE rowid = ?' % columns
            sql(update, (now, value, rowid))

            return value

    def decr(self, key, delta=1, default=0, retry=False):
        """Decrement value by delta for item with key.

        If key is missing and default is None then raise KeyError. Else if key
        is missing and default is not None then use default for value.

        Operation is atomic. All concurrent decrement operations will be
        counted individually.

        Unlike Memcached, negative values are supported. Value may be
        decremented below zero.

        Assumes value may be stored in a SQLite column. Most builds that target
        machines with 64-bit pointer widths will support 64-bit signed
        integers.

        Raises :exc:`Timeout` error when database timeout occurs and `retry` is
        `False` (default).

        :param key: key for item
        :param int delta: amount to decrement (default 1)
        :param int default: value if key is missing (default 0)
        :param bool retry: retry if database timeout occurs (default False)
        :return: new value for item
        :raises KeyError: if key is not found and default is None
        :raises Timeout: if database timeout occurs

        """
        return self.incr(key, -delta, default, retry)

    def get(
            self,
            key,
            default=None,
            read=False,
            expire_time=False,
            tag=False,
            retry=False,
    ):
        """
        从缓存中获取值。
        Raises :exc: 数据库超时且没有retry重试则抛出异常
        :param key: 缓存的key
        :param default: 设置的默认值，如果没有获取到，则返回此默认值
        :param bool read: 是否读取的是缓存文件
        :param bool expire_time: 是否返回过期时间
        :param bool tag: 是否返回tag标签
        :param bool retry: 如果超时是否重试
        """
        db_key, raw = self._disk.put(key)
        update_column = EVICTION_POLICY[self.eviction_policy]['get']
        select = (
            'SELECT rowid, expire_time, tag, mode, filename, value'
            ' FROM Cache WHERE key = ? AND raw = ?'
            ' AND (expire_time IS NULL OR expire_time > ?)'
        )

        if expire_time and tag:
            default = (default, None, None)
        elif expire_time or tag:
            default = (default, None)

        if not self.statistics and update_column is None:
            # Fast path, no transaction necessary.

            rows = self._sql(select, (db_key, raw, time.time())).fetchall()

            if not rows:
                return default

            ((rowid, db_expire_time, db_tag, mode, filename, db_value),) = rows

            try:
                value = self._disk.fetch(mode, filename, db_value, read)
            except IOError:
                # Key was deleted before we could retrieve result.
                return default

        else:  # Slow path, transaction required.
            cache_hit = (
                'UPDATE Settings SET value = value + 1 WHERE key = "hits"'
            )
            cache_miss = (
                'UPDATE Settings SET value = value + 1 WHERE key = "misses"'
            )

            with self._transact(retry) as (sql, _):
                rows = sql(select, (db_key, raw, time.time())).fetchall()

                if not rows:
                    if self.statistics:
                        sql(cache_miss)
                    return default

                (
                    (rowid, db_expire_time, db_tag, mode, filename, db_value),
                ) = rows  # noqa: E127

                try:
                    value = self._disk.fetch(mode, filename, db_value, read)
                except IOError:
                    # Key was deleted before we could retrieve result.
                    if self.statistics:
                        sql(cache_miss)
                    return default

                if self.statistics:
                    sql(cache_hit)

                now = time.time()
                update = 'UPDATE Cache SET %s WHERE rowid = ?'

                if update_column is not None:
                    sql(update % update_column.format(now=now), (rowid,))

        if expire_time and tag:
            return (value, db_expire_time, db_tag)
        elif expire_time:
            return (value, db_expire_time)
        elif tag:
            return (value, db_tag)
        else:
            return value

    def __getitem__(self, key):
        """Return corresponding value for `key` from cache.

        :param key: key matching item
        :return: corresponding value
        :raises KeyError: if key is not found

        """
        value = self.get(key, default=ENOVAL, retry=True)
        if value is ENOVAL:
            raise KeyError(key)
        return value

    def read(self, key, retry=False):
        """Return file handle value corresponding to `key` from cache.

        Raises :exc:`Timeout` error when database timeout occurs and `retry` is
        `False` (default).

        :param key: key matching item
        :param bool retry: retry if database timeout occurs (default False)
        :return: file open for reading in binary mode
        :raises KeyError: if key is not found
        :raises Timeout: if database timeout occurs

        """
        handle = self.get(key, default=ENOVAL, read=True, retry=retry)
        if handle is ENOVAL:
            raise KeyError(key)
        return handle

    def __contains__(self, key):
        """Return `True` if `key` matching item is found in cache.

        :param key: key matching item
        :return: True if key matching item

        """
        sql = self._sql
        db_key, raw = self._disk.put(key)
        select = (
            'SELECT rowid FROM Cache'
            ' WHERE key = ? AND raw = ?'
            ' AND (expire_time IS NULL OR expire_time > ?)'
        )

        rows = sql(select, (db_key, raw, time.time())).fetchall()

        return bool(rows)

    def pop(
            self, key, default=None, expire_time=False, tag=False, retry=False
    ):  # noqa: E501
        """Remove corresponding item for `key` from cache and return value.

        If `key` is missing, return `default`.

        Operation is atomic. Concurrent operations will be serialized.

        Raises :exc:`Timeout` error when database timeout occurs and `retry` is
        `False` (default).

        :param key: key for item
        :param default: value to return if key is missing (default None)
        :param bool expire_time: if True, return expire_time in tuple
            (default False)
        :param bool tag: if True, return tag in tuple (default False)
        :param bool retry: retry if database timeout occurs (default False)
        :return: value for item or default if key not found
        :raises Timeout: if database timeout occurs

        """
        db_key, raw = self._disk.put(key)
        select = (
            'SELECT rowid, expire_time, tag, mode, filename, value'
            ' FROM Cache WHERE key = ? AND raw = ?'
            ' AND (expire_time IS NULL OR expire_time > ?)'
        )

        if expire_time and tag:
            default = default, None, None
        elif expire_time or tag:
            default = default, None

        with self._transact(retry) as (sql, _):
            rows = sql(select, (db_key, raw, time.time())).fetchall()

            if not rows:
                return default

            ((rowid, db_expire_time, db_tag, mode, filename, db_value),) = rows

            sql('DELETE FROM Cache WHERE rowid = ?', (rowid,))

        try:
            value = self._disk.fetch(mode, filename, db_value, False)
        except IOError:
            # Key was deleted before we could retrieve result.
            return default
        finally:
            if filename is not None:
                self._disk.remove(filename)

        if expire_time and tag:
            return value, db_expire_time, db_tag
        elif expire_time:
            return value, db_expire_time
        elif tag:
            return value, db_tag
        else:
            return value

    def __delitem__(self, key, retry=True):
        """Delete corresponding item for `key` from cache.

        Raises :exc:`Timeout` error when database timeout occurs and `retry` is
        `False` (default `True`).

        :param key: key matching item
        :param bool retry: retry if database timeout occurs (default True)
        :raises KeyError: if key is not found
        :raises Timeout: if database timeout occurs

        """
        db_key, raw = self._disk.put(key)

        with self._transact(retry) as (sql, cleanup):
            rows = sql(
                'SELECT rowid, filename FROM Cache'
                ' WHERE key = ? AND raw = ?'
                ' AND (expire_time IS NULL OR expire_time > ?)',
                (db_key, raw, time.time()),
            ).fetchall()

            if not rows:
                raise KeyError(key)

            ((rowid, filename),) = rows
            sql('DELETE FROM Cache WHERE rowid = ?', (rowid,))
            cleanup(filename)

            return True

    def delete(self, key, retry=False):
        """Delete corresponding item for `key` from cache.

        Missing keys are ignored.

        Raises :exc:`Timeout` error when database timeout occurs and `retry` is
        `False` (default).

        :param key: key matching item
        :param bool retry: retry if database timeout occurs (default False)
        :return: True if item was deleted
        :raises Timeout: if database timeout occurs

        """
        # pylint: disable=unnecessary-dunder-call
        try:
            return self.__delitem__(key, retry=retry)
        except KeyError:
            return False

    def push(
            self,
            value,
            prefix=None,
            side='back',
            expire=None,
            read=False,
            tag=None,
            retry=False,
    ):
        """Push `value` onto `side` of queue identified by `prefix` in cache.

        When prefix is None, integer keys are used. Otherwise, string keys are
        used in the format "prefix-integer". Integer starts at 500 trillion.

        Defaults to pushing value on back of queue. Set side to 'front' to push
        value on front of queue. Side must be one of 'back' or 'front'.

        Operation is atomic. Concurrent operations will be serialized.

        When `read` is `True`, `value` should be a file-like object opened
        for reading in binary mode.

        Raises :exc:`Timeout` error when database timeout occurs and `retry` is
        `False` (default).

        See also `Cache.pull`.

        >>> cache = Cache()
        >>> print(cache.push('first value'))
        500000000000000
        >>> cache.get(500000000000000)
        'first value'
        >>> print(cache.push('second value'))
        500000000000001
        >>> print(cache.push('third value', side='front'))
        499999999999999
        >>> cache.push(1234, prefix='userids')
        'userids-500000000000000'

        :param value: value for item
        :param str prefix: key prefix (default None, key is integer)
        :param str side: either 'back' or 'front' (default 'back')
        :param float expire: seconds until the key expires
            (default None, no expiry)
        :param bool read: read value as bytes from file (default False)
        :param str tag: text to associate with key (default None)
        :param bool retry: retry if database timeout occurs (default False)
        :return: key for item in cache
        :raises Timeout: if database timeout occurs

        """
        if prefix is None:
            min_key = 0
            max_key = 999999999999999
        else:
            min_key = prefix + '-000000000000000'
            max_key = prefix + '-999999999999999'

        now = time.time()
        raw = True
        expire_time = None if expire is None else now + expire
        size, mode, filename, db_value = self._disk.store(value, read)
        columns = (expire_time, tag, size, mode, filename, db_value)
        order = {'back': 'DESC', 'front': 'ASC'}
        select = (
                     'SELECT key FROM Cache'
                     ' WHERE ? < key AND key < ? AND raw = ?'
                     ' ORDER BY key %s LIMIT 1'
                 ) % order[side]

        with self._transact(retry, filename) as (sql, cleanup):
            rows = sql(select, (min_key, max_key, raw)).fetchall()

            if rows:
                ((key,),) = rows

                if prefix is not None:
                    num = int(key[(key.rfind('-') + 1):])
                else:
                    num = key

                if side == 'back':
                    num += 1
                else:
                    assert side == 'front'
                    num -= 1
            else:
                num = 500000000000000

            if prefix is not None:
                db_key = '{0}-{1:015d}'.format(prefix, num)
            else:
                db_key = num

            self._row_insert(db_key, raw, now, columns)
            self._cull(now, sql, cleanup)

            return db_key

    def pull(
            self,
            prefix=None,
            default=(None, None),
            side='front',
            expire_time=False,
            tag=False,
            retry=False,
    ):
        """Pull key and value item pair from `side` of queue in cache.

        When prefix is None, integer keys are used. Otherwise, string keys are
        used in the format "prefix-integer". Integer starts at 500 trillion.

        If queue is empty, return default.

        Defaults to pulling key and value item pairs from front of queue. Set
        side to 'back' to pull from back of queue. Side must be one of 'front'
        or 'back'.

        Operation is atomic. Concurrent operations will be serialized.

        Raises :exc:`Timeout` error when database timeout occurs and `retry` is
        `False` (default).

        See also `Cache.push` and `Cache.get`.

        >>> cache = Cache()
        >>> cache.pull()
        (None, None)
        >>> for letter in 'abc':
        ...     print(cache.push(letter))
        500000000000000
        500000000000001
        500000000000002
        >>> key, value = cache.pull()
        >>> print(key)
        500000000000000
        >>> value
        'a'
        >>> _, value = cache.pull(side='back')
        >>> value
        'c'
        >>> cache.push(1234, 'userids')
        'userids-500000000000000'
        >>> _, value = cache.pull('userids')
        >>> value
        1234

        :param str prefix: key prefix (default None, key is integer)
        :param default: value to return if key is missing
            (default (None, None))
        :param str side: either 'front' or 'back' (default 'front')
        :param bool expire_time: if True, return expire_time in tuple
            (default False)
        :param bool tag: if True, return tag in tuple (default False)
        :param bool retry: retry if database timeout occurs (default False)
        :return: key and value item pair or default if queue is empty
        :raises Timeout: if database timeout occurs

        """
        # Caution: Nearly identical code exists in Cache.peek
        if prefix is None:
            min_key = 0
            max_key = 999999999999999
        else:
            min_key = prefix + '-000000000000000'
            max_key = prefix + '-999999999999999'

        order = {'front': 'ASC', 'back': 'DESC'}
        select = (
                     'SELECT rowid, key, expire_time, tag, mode, filename, value'
                     ' FROM Cache WHERE ? < key AND key < ? AND raw = 1'
                     ' ORDER BY key %s LIMIT 1'
                 ) % order[side]

        if expire_time and tag:
            default = default, None, None
        elif expire_time or tag:
            default = default, None

        while True:
            while True:
                with self._transact(retry) as (sql, cleanup):
                    rows = sql(select, (min_key, max_key)).fetchall()

                    if not rows:
                        return default

                    (
                        (rowid, key, db_expire, db_tag, mode, name, db_value),
                    ) = rows

                    sql('DELETE FROM Cache WHERE rowid = ?', (rowid,))

                    if db_expire is not None and db_expire < time.time():
                        cleanup(name)
                    else:
                        break

            try:
                value = self._disk.fetch(mode, name, db_value, False)
            except IOError:
                # Key was deleted before we could retrieve result.
                continue
            finally:
                if name is not None:
                    self._disk.remove(name)
            break

        if expire_time and tag:
            return (key, value), db_expire, db_tag
        elif expire_time:
            return (key, value), db_expire
        elif tag:
            return (key, value), db_tag
        else:
            return key, value

    def peek(
            self,
            prefix=None,
            default=(None, None),
            side='front',
            expire_time=False,
            tag=False,
            retry=False,
    ):
        """Peek at key and value item pair from `side` of queue in cache.

        When prefix is None, integer keys are used. Otherwise, string keys are
        used in the format "prefix-integer". Integer starts at 500 trillion.

        If queue is empty, return default.

        Defaults to peeking at key and value item pairs from front of queue.
        Set side to 'back' to pull from back of queue. Side must be one of
        'front' or 'back'.

        Expired items are deleted from cache. Operation is atomic. Concurrent
        operations will be serialized.

        Raises :exc:`Timeout` error when database timeout occurs and `retry` is
        `False` (default).

        See also `Cache.pull` and `Cache.push`.

        >>> cache = Cache()
        >>> for letter in 'abc':
        ...     print(cache.push(letter))
        500000000000000
        500000000000001
        500000000000002
        >>> key, value = cache.peek()
        >>> print(key)
        500000000000000
        >>> value
        'a'
        >>> key, value = cache.peek(side='back')
        >>> print(key)
        500000000000002
        >>> value
        'c'

        :param str prefix: key prefix (default None, key is integer)
        :param default: value to return if key is missing
            (default (None, None))
        :param str side: either 'front' or 'back' (default 'front')
        :param bool expire_time: if True, return expire_time in tuple
            (default False)
        :param bool tag: if True, return tag in tuple (default False)
        :param bool retry: retry if database timeout occurs (default False)
        :return: key and value item pair or default if queue is empty
        :raises Timeout: if database timeout occurs

        """
        # Caution: Nearly identical code exists in Cache.pull
        if prefix is None:
            min_key = 0
            max_key = 999999999999999
        else:
            min_key = prefix + '-000000000000000'
            max_key = prefix + '-999999999999999'

        order = {'front': 'ASC', 'back': 'DESC'}
        select = (
                     'SELECT rowid, key, expire_time, tag, mode, filename, value'
                     ' FROM Cache WHERE ? < key AND key < ? AND raw = 1'
                     ' ORDER BY key %s LIMIT 1'
                 ) % order[side]

        if expire_time and tag:
            default = default, None, None
        elif expire_time or tag:
            default = default, None

        while True:
            while True:
                with self._transact(retry) as (sql, cleanup):
                    rows = sql(select, (min_key, max_key)).fetchall()

                    if not rows:
                        return default

                    (
                        (rowid, key, db_expire, db_tag, mode, name, db_value),
                    ) = rows

                    if db_expire is not None and db_expire < time.time():
                        sql('DELETE FROM Cache WHERE rowid = ?', (rowid,))
                        cleanup(name)
                    else:
                        break

            try:
                value = self._disk.fetch(mode, name, db_value, False)
            except IOError:
                # Key was deleted before we could retrieve result.
                continue
            break

        if expire_time and tag:
            return (key, value), db_expire, db_tag
        elif expire_time:
            return (key, value), db_expire
        elif tag:
            return (key, value), db_tag
        else:
            return key, value

    def peekitem(self, last=True, expire_time=False, tag=False, retry=False):
        """Peek at key and value item pair in cache based on iteration order.

        Expired items are deleted from cache. Operation is atomic. Concurrent
        operations will be serialized.

        Raises :exc:`Timeout` error when database timeout occurs and `retry` is
        `False` (default).

        >>> cache = Cache()
        >>> for num, letter in enumerate('abc'):
        ...     cache[letter] = num
        >>> cache.peekitem()
        ('c', 2)
        >>> cache.peekitem(last=False)
        ('a', 0)

        :param bool last: last item in iteration order (default True)
        :param bool expire_time: if True, return expire_time in tuple
            (default False)
        :param bool tag: if True, return tag in tuple (default False)
        :param bool retry: retry if database timeout occurs (default False)
        :return: key and value item pair
        :raises KeyError: if cache is empty
        :raises Timeout: if database timeout occurs

        """
        order = ('ASC', 'DESC')
        select = (
                     'SELECT rowid, key, raw, expire_time, tag, mode, filename, value'
                     ' FROM Cache ORDER BY rowid %s LIMIT 1'
                 ) % order[last]

        while True:
            while True:
                with self._transact(retry) as (sql, cleanup):
                    rows = sql(select).fetchall()

                    if not rows:
                        raise KeyError('dictionary is empty')

                    (
                        (
                            rowid,
                            db_key,
                            raw,
                            db_expire,
                            db_tag,
                            mode,
                            name,
                            db_value,
                        ),
                    ) = rows

                    if db_expire is not None and db_expire < time.time():
                        sql('DELETE FROM Cache WHERE rowid = ?', (rowid,))
                        cleanup(name)
                    else:
                        break

            key = self._disk.get(db_key, raw)

            try:
                value = self._disk.fetch(mode, name, db_value, False)
            except IOError:
                # Key was deleted before we could retrieve result.
                continue
            break

        if expire_time and tag:
            return (key, value), db_expire, db_tag
        elif expire_time:
            return (key, value), db_expire
        elif tag:
            return (key, value), db_tag
        else:
            return key, value

    def memoize(
            self, name=None, typed=False, expire=None, tag=None, ignore=()
    ):
        """Memoizing cache decorator.

        Decorator to wrap callable with memoizing function using cache.
        Repeated calls with the same arguments will lookup result in cache and
        avoid function evaluation.

        If name is set to None (default), the callable name will be determined
        automatically.

        When expire is set to zero, function results will not be set in the
        cache. Cache lookups still occur, however. Read
        :doc:`case-study-landing-page-caching` for example usage.

        If typed is set to True, function arguments of different types will be
        cached separately. For example, f(3) and f(3.0) will be treated as
        distinct calls with distinct results.

        The original underlying function is accessible through the __wrapped__
        attribute. This is useful for introspection, for bypassing the cache,
        or for rewrapping the function with a different cache.

        >>> from zdppy_cache import Cache
        >>> cache = Cache()
        >>> @cache.memoize(expire=1, tag='fib')
        ... def fibonacci(number):
        ...     if number == 0:
        ...         return 0
        ...     elif number == 1:
        ...         return 1
        ...     else:
        ...         return fibonacci(number - 1) + fibonacci(number - 2)
        >>> print(fibonacci(100))
        354224848179261915075

        An additional `__cache_key__` attribute can be used to generate the
        cache key used for the given arguments.

        >>> key = fibonacci.__cache_key__(100)
        >>> print(cache[key])
        354224848179261915075

        Remember to call memoize when decorating a callable. If you forget,
        then a TypeError will occur. Note the lack of parenthenses after
        memoize below:

        >>> @cache.memoize
        ... def test():
        ...     pass
        Traceback (most recent call last):
            ...
        TypeError: name cannot be callable

        :param cache: cache to store callable arguments and return values
        :param str name: name given for callable (default None, automatic)
        :param bool typed: cache different types separately (default False)
        :param float expire: seconds until arguments expire
            (default None, no expiry)
        :param str tag: text to associate with arguments (default None)
        :param set ignore: positional or keyword args to ignore (default ())
        :return: callable decorator

        """
        # Caution: Nearly identical code exists in DjangoCache.memoize
        if callable(name):
            raise TypeError('name cannot be callable')

        def decorator(func):
            """Decorator created by memoize() for callable `func`."""
            base = (full_name(func),) if name is None else (name,)

            @ft.wraps(func)
            def wrapper(*args, **kwargs):
                """Wrapper for callable to cache arguments and return values."""
                key = wrapper.__cache_key__(*args, **kwargs)
                result = self.get(key, default=ENOVAL, retry=True)

                if result is ENOVAL:
                    result = func(*args, **kwargs)
                    if expire is None or expire > 0:
                        self.set(key, result, expire, tag=tag, retry=True)

                return result

            def __cache_key__(*args, **kwargs):
                """Make key for cache given function arguments."""
                return args_to_key(base, args, kwargs, typed, ignore)

            wrapper.__cache_key__ = __cache_key__
            return wrapper

        return decorator

    def check(self, fix=False, retry=False):
        """Check database and file system consistency.

        Intended for use in testing and post-mortem error analysis.

        While checking the Cache table for consistency, a writer lock is held
        on the database. The lock blocks other cache clients from writing to
        the database. For caches with many file references, the lock may be
        held for a long time. For example, local benchmarking shows that a
        cache with 1,000 file references takes ~60ms to check.

        Raises :exc:`Timeout` error when database timeout occurs and `retry` is
        `False` (default).

        :param bool fix: correct inconsistencies
        :param bool retry: retry if database timeout occurs (default False)
        :return: list of warnings
        :raises Timeout: if database timeout occurs

        """
        # pylint: disable=access-member-before-definition,W0201
        with warnings.catch_warnings(record=True) as warns:
            sql = self._sql

            # Check integrity of database.

            rows = sql('PRAGMA integrity_check').fetchall()

            if len(rows) != 1 or rows[0][0] != 'ok':
                for (message,) in rows:
                    warnings.warn(message)

            if fix:
                sql('VACUUM')

            with self._transact(retry) as (sql, _):

                # Check Cache.filename against file system.

                filenames = set()
                select = (
                    'SELECT rowid, size, filename FROM Cache'
                    ' WHERE filename IS NOT NULL'
                )

                rows = sql(select).fetchall()

                for rowid, size, filename in rows:
                    full_path = op.join(self._directory, filename)
                    filenames.add(full_path)

                    if op.exists(full_path):
                        real_size = op.getsize(full_path)

                        if size != real_size:
                            message = 'wrong file size: %s, %d != %d'
                            args = full_path, real_size, size
                            warnings.warn(message % args)

                            if fix:
                                sql(
                                    'UPDATE Cache SET size = ?'
                                    ' WHERE rowid = ?',
                                    (real_size, rowid),
                                )

                        continue

                    warnings.warn('file not found: %s' % full_path)

                    if fix:
                        sql('DELETE FROM Cache WHERE rowid = ?', (rowid,))

                # Check file system against Cache.filename.

                for dirpath, _, files in os.walk(self._directory):
                    paths = [op.join(dirpath, filename) for filename in files]
                    error = set(paths) - filenames

                    for full_path in error:
                        if DBNAME in full_path:
                            continue

                        message = 'unknown file: %s' % full_path
                        warnings.warn(message, UnknownFileWarning)

                        if fix:
                            os.remove(full_path)

                # Check for empty directories.

                for dirpath, dirs, files in os.walk(self._directory):
                    if not (dirs or files):
                        message = 'empty directory: %s' % dirpath
                        warnings.warn(message, EmptyDirWarning)

                        if fix:
                            os.rmdir(dirpath)

                # Check Settings.count against count of Cache rows.

                self.reset('count')
                ((count,),) = sql('SELECT COUNT(key) FROM Cache').fetchall()

                if self.count != count:
                    message = 'Settings.count != COUNT(Cache.key); %d != %d'
                    warnings.warn(message % (self.count, count))

                    if fix:
                        sql(
                            'UPDATE Settings SET value = ? WHERE key = ?',
                            (count, 'count'),
                        )

                # Check Settings.size against sum of Cache.size column.

                self.reset('size')
                select_size = 'SELECT COALESCE(SUM(size), 0) FROM Cache'
                ((size,),) = sql(select_size).fetchall()

                if self.size != size:
                    message = 'Settings.size != SUM(Cache.size); %d != %d'
                    warnings.warn(message % (self.size, size))

                    if fix:
                        sql(
                            'UPDATE Settings SET value = ? WHERE key =?',
                            (size, 'size'),
                        )

            return warns

    def create_tag_index(self):
        """Create tag index on cache database.

        It is better to initialize cache with `tag_index=True` than use this.

        :raises Timeout: if database timeout occurs

        """
        sql = self._sql
        sql('CREATE INDEX IF NOT EXISTS Cache_tag_rowid ON Cache(tag, rowid)')
        self.reset('tag_index', 1)

    def drop_tag_index(self):
        """Drop tag index on cache database.

        :raises Timeout: if database timeout occurs

        """
        sql = self._sql
        sql('DROP INDEX IF EXISTS Cache_tag_rowid')
        self.reset('tag_index', 0)

    def evict(self, tag, retry=False):
        """Remove items with matching `tag` from cache.

        Removing items is an iterative process. In each iteration, a subset of
        items is removed. Concurrent writes may occur between iterations.

        If a :exc:`Timeout` occurs, the first element of the exception's
        `args` attribute will be the number of items removed before the
        exception occurred.

        Raises :exc:`Timeout` error when database timeout occurs and `retry` is
        `False` (default).

        :param str tag: tag identifying items
        :param bool retry: retry if database timeout occurs (default False)
        :return: count of rows removed
        :raises Timeout: if database timeout occurs

        """
        select = (
            'SELECT rowid, filename FROM Cache'
            ' WHERE tag = ? AND rowid > ?'
            ' ORDER BY rowid LIMIT ?'
        )
        args = [tag, 0, 100]
        return self._select_delete(select, args, arg_index=1, retry=retry)

    def expire(self, now=None, retry=False):
        """
        删除过期的缓存信息
        :param float now: 当前时间的秒值
        :param bool retry: 是否重试
        :return: 被删除的数量
        """
        select = (
            'SELECT rowid, expire_time, filename FROM Cache'
            ' WHERE ? < expire_time AND expire_time < ?'
            ' ORDER BY expire_time LIMIT ?'
        )
        args = [0, now or time.time(), 100]
        count = self._select_delete(select, args, row_index=1, retry=retry)
        print("xxxxxxxxxxx清除过期内容", count)
        return count

    def cull(self, retry=False):
        """Cull items from cache until volume is less than size limit.

        Removing items is an iterative process. In each iteration, a subset of
        items is removed. Concurrent writes may occur between iterations.

        If a :exc:`Timeout` occurs, the first element of the exception's
        `args` attribute will be the number of items removed before the
        exception occurred.

        Raises :exc:`Timeout` error when database timeout occurs and `retry` is
        `False` (default).

        :param bool retry: retry if database timeout occurs (default False)
        :return: count of items removed
        :raises Timeout: if database timeout occurs

        """
        now = time.time()

        # Remove expired items.

        count = self.expire(now)

        # Remove items by policy.

        select_policy = EVICTION_POLICY[self.eviction_policy]['cull']

        if select_policy is None:
            return 0

        select_filename = select_policy.format(fields='filename', now=now)

        try:
            while self.volume() > self.size_limit:
                with self._transact(retry) as (sql, cleanup):
                    rows = sql(select_filename, (10,)).fetchall()

                    if not rows:
                        break

                    count += len(rows)
                    delete = (
                            'DELETE FROM Cache WHERE rowid IN (%s)'
                            % select_policy.format(fields='rowid', now=now)
                    )
                    sql(delete, (10,))

                    for (filename,) in rows:
                        cleanup(filename)
        except Timeout:
            raise Timeout(count) from None

        return count

    def clear(self, retry=False):
        """
        清空所有的缓存对象
        移除项目是一个迭代过程。在每次迭代中，移除项目的一个子集。在迭代之间可能发生并发写。
        :param bool retry: 是否重试
        :return: 被移除的数量
        """
        select = (
            'SELECT rowid, filename FROM Cache'
            ' WHERE rowid > ?'
            ' ORDER BY rowid LIMIT ?'
        )
        args = [0, 100]
        return self._select_delete(select, args, retry=retry)

    def _select_delete(
            self, select, args, row_index=0, arg_index=0, retry=False
    ):
        count = 0
        delete = 'DELETE FROM Cache WHERE rowid IN (%s)'

        try:
            while True:
                with self._transact(retry) as (sql, cleanup):
                    rows = sql(select, args).fetchall()

                    if not rows:
                        break

                    count += len(rows)
                    sql(delete % ','.join(str(row[0]) for row in rows))

                    for row in rows:
                        args[arg_index] = row[row_index]
                        cleanup(row[-1])

        except Timeout:
            raise Timeout(count) from None

        return count

    def get_all_keys(self, is_active=True, limit=100000):
        """
        遍历数据库中所有的key，默认查询所有没过期的
        :param is_active: 是否只查没过期的
        :param limit: 默认10000，但是允许做限制
        :return: 遍历到的所有的key，没有返回空列表
        """
        _disk_get = self._disk.get

        rows = None
        if is_active:
            # 查没过期的
            select = 'SELECT key FROM Cache where expire_time > ? LIMIT ?'
            rows = self._sql(select, (time.time(), limit)).fetchall()
        else:
            # 查所有的
            select = 'SELECT key FROM Cache  LIMIT ?'
            rows = self._sql(select, (limit,)).fetchall()

        # 返回，这里rows不可能为None，所以可以这么写
        return [v[0] for v in rows]

    def get_all_items(self, is_active=True, limit=100000):
        """
        遍历数据库中所有的key，默认查询所有没过期的
        :param is_active: 是否只查没过期的
        :param limit: 默认10000，但是允许做限制
        :return: 遍历到的所有的key，没有返回空列表
        """
        _disk_get = self._disk.get

        rows = None
        if is_active:
            # 查没过期的
            select = 'SELECT key,value FROM Cache where expire_time > ? LIMIT ?'
            rows = self._sql(select, (time.time(), limit)).fetchall()
        else:
            # 查所有的
            select = 'SELECT key,value FROM Cache  LIMIT ?'
            rows = self._sql(select, (limit,)).fetchall()

        # 返回，这里rows不可能为None，所以可以这么写
        return {v[0]: v[1] for v in rows}

    def get_all(self, is_active=True, limit=100000):
        """
        遍历数据库中所有的key，默认查询所有没过期的
        :param is_active: 是否只查没过期的
        :param limit: 默认10000，但是允许做限制
        :return: 遍历到的所有的key，没有返回空列表
        """
        _disk_get = self._disk.get

        columns = ["key", "raw", "store_time", "expire_time", "access_time", "access_count", "tag", "size", "mode",
                   "filename", "value"]
        column = ",".join(columns)
        rows = None
        if is_active:
            # 查没过期的
            select = f'SELECT {column} FROM Cache where expire_time > ? LIMIT ?'
            rows = self._sql(select, (time.time(), limit)).fetchall()
        else:
            # 查所有的
            select = f'SELECT {column} FROM Cache  LIMIT ?'
            rows = self._sql(select, (limit,)).fetchall()

        # 处理
        data = []
        for row in rows:
            item = {}
            for i in range(len(columns)):
                item[columns[i]] = row[i]
            data.append(item)

        # 返回
        return data

    def iterkeys(self, reverse=False):
        """
        遍历数据库中所有的key，会排序
        :param bool reverse: 是否反序
        :return: 遍历到的所有的key
        """
        sql = self._sql
        limit = 100
        _disk_get = self._disk.get

        # 拼接SQL，因为要做排序，所以要先查出排序的第一条来，后面根据这个继续迭代查询
        if reverse:
            select = 'SELECT key, raw FROM Cache ORDER BY key DESC, raw DESC LIMIT 1'
            iterate = 'SELECT key, raw FROM Cache WHERE key = ? AND raw < ? OR key < ? ORDER BY key DESC, raw DESC LIMIT ?'
        else:
            select = 'SELECT key, raw FROM Cache ORDER BY key ASC, raw ASC LIMIT 1'
            iterate = 'SELECT key, raw FROM Cache WHERE key = ? AND raw > ? OR key > ? ORDER BY key ASC, raw ASC LIMIT ?'

        # 执行查询
        row = sql(select).fetchall()

        # 判断是否有结果
        if row:
            ((key, raw),) = row
        else:
            return

        # 封装生成器
        yield _disk_get(key, raw)
        while True:
            rows = sql(iterate, (key, raw, key, limit)).fetchall()
            if not rows:
                break
            for key, raw in rows:
                yield _disk_get(key, raw)

    def _iter(self, ascending=True):
        sql = self._sql
        rows = sql('SELECT MAX(rowid) FROM Cache').fetchall()
        ((max_rowid,),) = rows
        yield  # Signal ready.

        if max_rowid is None:
            return

        bound = max_rowid + 1
        limit = 100
        _disk_get = self._disk.get
        rowid = 0 if ascending else bound
        select = (
                     'SELECT rowid, key, raw FROM Cache'
                     ' WHERE ? < rowid AND rowid < ?'
                     ' ORDER BY rowid %s LIMIT ?'
                 ) % ('ASC' if ascending else 'DESC')

        while True:
            if ascending:
                args = (rowid, bound, limit)
            else:
                args = (0, rowid, limit)

            rows = sql(select, args).fetchall()

            if not rows:
                break

            for rowid, key, raw in rows:
                yield _disk_get(key, raw)

    def __iter__(self):
        """Iterate keys in cache including expired items."""
        iterator = self._iter()
        next(iterator)
        return iterator

    def __reversed__(self):
        """Reverse iterate keys in cache including expired items."""
        iterator = self._iter(ascending=False)
        next(iterator)
        return iterator

    def stats(self, enable=True, reset=False):
        """Return cache statistics hits and misses.

        :param bool enable: enable collecting statistics (default True)
        :param bool reset: reset hits and misses to 0 (default False)
        :return: (hits, misses)

        """
        # pylint: disable=E0203,W0201
        result = (self.reset('hits'), self.reset('misses'))

        if reset:
            self.reset('hits', 0)
            self.reset('misses', 0)

        self.reset('statistics', enable)

        return result

    def volume(self):
        """
        返回磁盘上缓存的估计总大小。
        :return: 字节大小
        """
        ((page_count,),) = self._sql('PRAGMA page_count').fetchall()
        total_size = self._page_size * page_count + self.reset('size')
        return total_size

    def close(self):
        """
        关闭数据库的连接
        """
        con = getattr(self._local, 'con', None)

        if con is None:
            return

        con.close()

        try:
            delattr(self._local, 'con')
        except AttributeError:
            pass

    def __enter__(self):
        # Create connection in thread.
        # pylint: disable=unused-variable
        connection = self._con  # noqa
        return self

    def __exit__(self, *exception):
        self.close()

    def __len__(self):
        """Count of items in cache including expired items."""
        return self.reset('count')

    def __getstate__(self):
        return (self.directory, self.timeout, type(self.disk))

    def __setstate__(self, state):
        self.__init__(*state)

    def reset(self, key, value=ENOVAL, update=True):
        """Reset `key` and `value` item from Settings table.

        Use `reset` to update the value of Cache settings correctly. Cache
        settings are stored in the Settings table of the SQLite database. If
        `update` is ``False`` then no attempt is made to update the database.

        If `value` is not given, it is reloaded from the Settings
        table. Otherwise, the Settings table is updated.

        Settings with the ``disk_`` prefix correspond to Disk
        attributes. Updating the value will change the unprefixed attribute on
        the associated Disk instance.

        Settings with the ``sqlite_`` prefix correspond to SQLite
        pragmas. Updating the value will execute the corresponding PRAGMA
        statement.

        SQLite PRAGMA statements may be executed before the Settings table
        exists in the database by setting `update` to ``False``.

        :param str key: Settings key for item
        :param value: value for item (optional)
        :param bool update: update database Settings table (default True)
        :return: updated value for item
        :raises Timeout: if database timeout occurs

        """
        sql = self._sql
        sql_retry = self._sql_retry

        if value is ENOVAL:
            select = 'SELECT value FROM Settings WHERE key = ?'
            ((value,),) = sql_retry(select, (key,)).fetchall()
            setattr(self, key, value)
            return value

        if update:
            statement = 'UPDATE Settings SET value = ? WHERE key = ?'
            sql_retry(statement, (value, key))

        if key.startswith('sqlite_'):
            pragma = key[7:]

            # 2016-02-17 GrantJ - PRAGMA and isolation_level=None
            # don't always play nicely together. Retry setting the
            # PRAGMA. I think some PRAGMA statements expect to
            # immediately take an EXCLUSIVE lock on the database. I
            # can't find any documentation for this but without the
            # retry, stress will intermittently fail with multiple
            # processes.

            # 2018-11-05 GrantJ - Avoid setting pragma values that
            # are already set. Pragma settings like auto_vacuum and
            # journal_mode can take a long time or may not work after
            # tables have been created.

            start = time.time()
            while True:
                try:
                    try:
                        ((old_value,),) = sql(
                            'PRAGMA %s' % (pragma)
                        ).fetchall()
                        update = old_value != value
                    except ValueError:
                        update = True
                    if update:
                        sql('PRAGMA %s = %s' % (pragma, value)).fetchall()
                    break
                except sqlite3.OperationalError as exc:
                    if str(exc) != 'database is locked':
                        raise
                    diff = time.time() - start
                    if diff > 60:
                        raise
                    time.sleep(0.001)
        elif key.startswith('disk_'):
            attr = key[5:]
            setattr(self._disk, attr, value)

        setattr(self, key, value)
        return value
