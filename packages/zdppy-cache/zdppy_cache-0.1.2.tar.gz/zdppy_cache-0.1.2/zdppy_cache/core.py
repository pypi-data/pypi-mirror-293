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


def full_name(func):
    """Return full name of `func` by adding the module and function name."""
    return func.__module__ + '.' + func.__qualname__


class Constant(tuple):
    """Pretty display of immutable constant."""

    def __new__(cls, name):
        return tuple.__new__(cls, (name,))

    def __repr__(self):
        return '%s' % self[0]


DBNAME = 'cache.db'
ENOVAL = Constant('ENOVAL')
UNKNOWN = Constant('UNKNOWN')

MODE_NONE = 0
MODE_RAW = 1
MODE_BINARY = 2
MODE_TEXT = 3
MODE_PICKLE = 4

# 默认配置
DEFAULT_SETTINGS = {
    'statistics': 0,  # False
    'tag_index': 0,  # False
    'eviction_policy': 'least-recently-stored',
    'size_limit': 2 ** 30,  # 1gb
    'cull_limit': 10,
    'sqlite_auto_vacuum': 1,  # FULL
    'sqlite_cache_size': 2 ** 13,  # 8,192 pages
    'sqlite_journal_mode': 'wal',
    'sqlite_mmap_size': 2 ** 26,  # 64mb
    'sqlite_synchronous': 1,  # NORMAL
    'disk_min_file_size': 2 ** 15,  # 32kb
    'disk_pickle_protocol': pickle.HIGHEST_PROTOCOL,
}

METADATA = {
    'count': 0,
    'size': 0,
    'hits': 0,
    'misses': 0,
}

EVICTION_POLICY = {
    'none': {
        'init': None,
        'get': None,
        'cull': None,
    },
    'least-recently-stored': {
        'init': (
            'CREATE INDEX IF NOT EXISTS Cache_store_time ON'
            ' Cache (store_time)'
        ),
        'get': None,
        'cull': 'SELECT {fields} FROM Cache ORDER BY store_time LIMIT ?',
    },
    'least-recently-used': {
        'init': (
            'CREATE INDEX IF NOT EXISTS Cache_access_time ON'
            ' Cache (access_time)'
        ),
        'get': 'access_time = {now}',
        'cull': 'SELECT {fields} FROM Cache ORDER BY access_time LIMIT ?',
    },
    'least-frequently-used': {
        'init': (
            'CREATE INDEX IF NOT EXISTS Cache_access_count ON'
            ' Cache (access_count)'
        ),
        'get': 'access_count = access_count + 1',
        'cull': 'SELECT {fields} FROM Cache ORDER BY access_count LIMIT ?',
    },
}


class Disk:
    """Cache key and value serialization for SQLite database and files."""

    def __init__(self, directory, min_file_size=0, pickle_protocol=0):
        """Initialize disk instance.

        :param str directory: directory path
        :param int min_file_size: minimum size for file use
        :param int pickle_protocol: pickle protocol for serialization

        """
        self._directory = directory
        self.min_file_size = min_file_size
        self.pickle_protocol = pickle_protocol

    def hash(self, key):
        """Compute portable hash for `key`.

        :param key: key to hash
        :return: hash value

        """
        mask = 0xFFFFFFFF
        disk_key, _ = self.put(key)
        type_disk_key = type(disk_key)

        if type_disk_key is sqlite3.Binary:
            return zlib.adler32(disk_key) & mask
        elif type_disk_key is str:
            return zlib.adler32(disk_key.encode('utf-8')) & mask  # noqa
        elif type_disk_key is int:
            return disk_key % mask
        else:
            assert type_disk_key is float
            return zlib.adler32(struct.pack('!d', disk_key)) & mask

    def put(self, key):
        """Convert `key` to fields key and raw for Cache table.

        :param key: key to convert
        :return: (database key, raw boolean) pair

        """
        # pylint: disable=unidiomatic-typecheck
        type_key = type(key)

        if type_key is bytes:
            return sqlite3.Binary(key), True
        elif (
                (type_key is str)
                or (
                        type_key is int
                        and -9223372036854775808 <= key <= 9223372036854775807
                )
                or (type_key is float)
        ):
            return key, True
        else:
            data = pickle.dumps(key, protocol=self.pickle_protocol)
            result = pickletools.optimize(data)
            return sqlite3.Binary(result), False

    def get(self, key, raw):
        """Convert fields `key` and `raw` from Cache table to key.

        :param key: database key to convert
        :param bool raw: 标记缓存的对象是否为文本
        :return: corresponding Python key

        """
        # pylint: disable=unidiomatic-typecheck
        if raw:
            return bytes(key) if type(key) is sqlite3.Binary else key
        else:
            return pickle.load(io.BytesIO(key))

    def store(self, value, read, key=UNKNOWN):
        """Convert `value` to fields size, mode, filename, and value for Cache
        table.

        :param value: value to convert
        :param bool read: True when value is file-like object
        :param key: key for item (default UNKNOWN)
        :return: (size, mode, filename, value) tuple for Cache table

        """
        # pylint: disable=unidiomatic-typecheck
        type_value = type(value)
        min_file_size = self.min_file_size

        if (
                (type_value is str and len(value) < min_file_size)
                or (
                type_value is int
                and -9223372036854775808 <= value <= 9223372036854775807
        )
                or (type_value is float)
        ):
            return 0, MODE_RAW, None, value
        elif type_value is bytes:
            if len(value) < min_file_size:
                return 0, MODE_RAW, None, sqlite3.Binary(value)
            else:
                filename, full_path = self.filename(key, value)
                self._write(full_path, io.BytesIO(value), 'xb')
                return len(value), MODE_BINARY, filename, None
        elif type_value is str:
            filename, full_path = self.filename(key, value)
            self._write(full_path, io.StringIO(value), 'x', 'UTF-8')
            size = op.getsize(full_path)
            return size, MODE_TEXT, filename, None
        elif read:
            reader = ft.partial(value.read, 2 ** 22)
            filename, full_path = self.filename(key, value)
            iterator = iter(reader, b'')
            size = self._write(full_path, iterator, 'xb')
            return size, MODE_BINARY, filename, None
        else:
            result = pickle.dumps(value, protocol=self.pickle_protocol)

            if len(result) < min_file_size:
                return 0, MODE_PICKLE, None, sqlite3.Binary(result)
            else:
                filename, full_path = self.filename(key, value)
                self._write(full_path, io.BytesIO(result), 'xb')
                return len(result), MODE_PICKLE, filename, None

    def _write(self, full_path, iterator, mode, encoding=None):
        full_dir, _ = op.split(full_path)

        for count in range(1, 11):
            with cl.suppress(OSError):
                os.makedirs(full_dir)

            try:
                # Another cache may have deleted the directory before
                # the file could be opened.
                writer = open(full_path, mode, encoding=encoding)
            except OSError:
                if count == 10:
                    # Give up after 10 tries to open the file.
                    raise
                continue

            with writer:
                size = 0
                for chunk in iterator:
                    size += len(chunk)
                    writer.write(chunk)
                return size

    def fetch(self, mode, filename, value, read):
        """Convert fields `mode`, `filename`, and `value` from Cache table to
        value.

        :param int mode: value mode raw, binary, text, or pickle
        :param str filename: filename of corresponding value
        :param value: database value
        :param bool read: when True, return an open file handle
        :return: corresponding Python value
        :raises: IOError if the value cannot be read

        """
        # pylint: disable=unidiomatic-typecheck,consider-using-with
        if mode == MODE_RAW:
            return bytes(value) if type(value) is sqlite3.Binary else value
        elif mode == MODE_BINARY:
            if read:
                return open(op.join(self._directory, filename), 'rb')
            else:
                with open(op.join(self._directory, filename), 'rb') as reader:
                    return reader.read()
        elif mode == MODE_TEXT:
            full_path = op.join(self._directory, filename)
            with open(full_path, 'r', encoding='UTF-8') as reader:
                return reader.read()
        elif mode == MODE_PICKLE:
            if value is None:
                with open(op.join(self._directory, filename), 'rb') as reader:
                    return pickle.load(reader)
            else:
                return pickle.load(io.BytesIO(value))

    def filename(self, key=UNKNOWN, value=UNKNOWN):
        """Return filename and full-path tuple for file storage.

        Filename will be a randomly generated 28 character hexadecimal string
        with ".val" suffixed. Two levels of sub-directories will be used to
        reduce the size of directories. On older filesystems, lookups in
        directories with many files may be slow.

        The default implementation ignores the `key` and `value` parameters.

        In some scenarios, for example :meth:`Cache.push
        <zdppy_cache.Cache.push>`, the `key` or `value` may not be known when the
        item is stored in the cache.

        :param key: key for item (default UNKNOWN)
        :param value: value for item (default UNKNOWN)

        """
        # pylint: disable=unused-argument
        hex_name = codecs.encode(os.urandom(16), 'hex').decode('utf-8')
        sub_dir = op.join(hex_name[:2], hex_name[2:4])
        name = hex_name[4:] + '.val'
        filename = op.join(sub_dir, name)
        full_path = op.join(self._directory, filename)
        return filename, full_path

    def remove(self, file_path):
        """Remove a file given by `file_path`.

        This method is cross-thread and cross-process safe. If an OSError
        occurs, it is suppressed.

        :param str file_path: relative path to file

        """
        full_path = op.join(self._directory, file_path)
        full_dir, _ = op.split(full_path)

        # Suppress OSError that may occur if two caches attempt to delete the
        # same file or directory at the same time.

        with cl.suppress(OSError):
            os.remove(full_path)

        with cl.suppress(OSError):
            os.removedirs(full_dir)


class JSONDisk(Disk):
    """Cache key and value using JSON serialization with zlib compression."""

    def __init__(self, directory, compress_level=1, **kwargs):
        """Initialize JSON disk instance.

        Keys and values are compressed using the zlib library. The
        `compress_level` is an integer from 0 to 9 controlling the level of
        compression; 1 is fastest and produces the least compression, 9 is
        slowest and produces the most compression, and 0 is no compression.

        :param str directory: directory path
        :param int compress_level: zlib compression level (default 1)
        :param kwargs: super class arguments

        """
        self.compress_level = compress_level
        super().__init__(directory, **kwargs)

    def put(self, key):
        json_bytes = json.dumps(key).encode('utf-8')
        data = zlib.compress(json_bytes, self.compress_level)
        return super().put(data)

    def get(self, key, raw):
        data = super().get(key, raw)
        return json.loads(zlib.decompress(data).decode('utf-8'))

    def store(self, value, read, key=UNKNOWN):
        if not read:
            json_bytes = json.dumps(value).encode('utf-8')
            value = zlib.compress(json_bytes, self.compress_level)
        return super().store(value, read, key=key)

    def fetch(self, mode, filename, value, read):
        data = super().fetch(mode, filename, value, read)
        if not read:
            data = json.loads(zlib.decompress(data).decode('utf-8'))
        return data


class Timeout(Exception):
    """Database timeout expired."""


class UnknownFileWarning(UserWarning):
    """Warning used by Cache.check for unknown files."""


class EmptyDirWarning(UserWarning):
    """Warning used by Cache.check for empty directories."""


def args_to_key(base, args, kwargs, typed, ignore):
    """Create cache key out of function arguments.

    :param tuple base: base of key
    :param tuple args: function arguments
    :param dict kwargs: function keyword arguments
    :param bool typed: include types in cache key
    :param set ignore: positional or keyword args to ignore
    :return: cache key tuple

    """
    args = tuple(arg for index, arg in enumerate(args) if index not in ignore)
    key = base + args + (None,)

    if kwargs:
        kwargs = {key: val for key, val in kwargs.items() if key not in ignore}
        sorted_items = sorted(kwargs.items())

        for item in sorted_items:
            key += item

    if typed:
        key += tuple(type(arg) for arg in args)

        if kwargs:
            key += tuple(type(value) for _, value in sorted_items)

    return key

