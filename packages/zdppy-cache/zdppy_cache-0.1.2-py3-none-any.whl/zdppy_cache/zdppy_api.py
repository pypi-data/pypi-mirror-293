from .user_cache import UserCache
from .cache import Cache


def cache(key1, key2, api):
    """
    生成缓存相关的接口
    :param key1: 管理员的第一个加密key
    :param key2: 管理员的第二个加密key
    :param api: zdppy_api 的包
    :return:
    """
    # 管理员的缓存对象
    admin_cache = UserCache(key1, key2)
    # 用户缓存字典
    user_cache_dict = {}

    def get_cache(req):
        """获取缓存对象"""
        # 获取请求头参数
        ukey1 = api.req.get_header(req, "key1")
        ukey2 = api.req.get_header(req, "key2")
        if ukey1 is None or ukey2 is None:
            return None, "key1或key2不能为空"

        # 管理员
        if ukey1 == key1 and ukey2 == key2:
            return admin_cache, None

        # 普通用户
        # 判断用户缓存对象是否已存在
        cache_obj = user_cache_dict.get(ukey1, None)
        if cache_obj is None:
            # 用户
            cache_obj = UserCache(ukey1, ukey2)
            # 管理员缓存用户目录：用户名=>缓存目录
            admin_cache.set(ukey1, cache_obj.cache_dir)

        # 返回
        return cache_obj, None

    # 管理员
    async def set(req):
        """设置缓存的接口"""
        # 获取缓存对象
        cache_obj, err = get_cache(req)
        if err:
            return api.resp.error_400(err)

        # 设置缓存
        data = await api.req.get_json(req)
        key = data.get("key")
        value = data.get("value")
        expire = data.get("expire")
        if not expire:
            expire = 180
        cache_obj.set(key, value, expire)
        return api.resp.success()

    async def get(req):
        """获取缓存的接口"""
        # 获取缓存对象
        cache_obj, err = get_cache(req)
        if err is not None:
            return api.resp.error_400(err)

        # 获取key
        data = await api.req.get_json(req)
        key = data.get("key")

        # 获取缓存
        value = cache_obj.get(key)
        if not value:
            return api.resp.error_404()
        return api.resp.success({"key": key, "value": value})

    async def query(req):
        """查询缓存的接口"""
        # 获取缓存对象
        cache_obj, err = get_cache(req)
        if err is not None:
            return api.resp.error_400(err)

        # 获取查询参数
        params = await api.req.get_json(req)

        # 默认查询所有key
        data = cache_obj.get_all_keys(False)
        if params.get("error"):  # 什么参数都没有传
            return api.resp.success({
                "query": params,
                "data": data,
            })

        # 是否包含值
        has_value = params.get("value")
        # 是否返回详细信息
        has_detail = params.get("detail")
        # 是否只获取激活的
        has_active = params.get("active")
        if has_active:
            # 只查询未过期的
            if has_detail:
                data = cache_obj.get_all()
            elif has_value:
                data = cache_obj.get_all_items()
            else:
                data = cache_obj.get_all_keys()
        else:
            # 查询所有的
            if has_detail:
                data = cache_obj.get_all(False)
            elif has_value:
                data = cache_obj.get_all_items(False)
            else:
                data = cache_obj.get_all_keys(False)
        return api.resp.success({
            "query": params,
            "data": data,
        })

    async def delete(req):
        """删除缓存的接口"""
        # 获取缓存对象
        cache_obj, err = get_cache(req)
        if err is not None:
            return api.resp.error_400(err)

        # 获取查询参数
        data = await api.req.get_json(req)
        key = data.get("key")

        # 删除缓存
        cache_obj.delete(key)
        return api.resp.success()

    async def resize(req):
        """重置缓存"""
        # 获取缓存对象
        cache_obj, err = get_cache(req)
        if err is not None:
            return api.resp.error_400(err)

        # 删除前大小
        old_size = cache_obj.get_size()

        # 获取要保留的过期缓存个数
        json_data = await api.req.get_json(req)
        limit = json_data.get("limit")
        if not limit:
            limit = 1000
        # 删除过期的缓存
        cache_obj.resize(False, limit)
        new_size = cache_obj.get_size()

        # 返回
        data = {"old_size": old_size, "new_size": new_size}
        return api.resp.success(data)

    async def get_size(req):
        """获取缓存对象"""
        # 获取缓存对象
        cache_obj, err = get_cache(req)
        if err is not None:
            return api.resp.error_400(err)

        # 查询缓存大小
        size = cache_obj.get_size()
        return api.resp.success({"size": size})

    async def delete_all(req):
        """清空缓存"""
        # 获取缓存对象
        cache_obj, err = get_cache(req)
        if err is not None:
            return api.resp.error_400(err)
        # 删除所有缓存
        cache_obj.delete_all()
        return api.resp.success()

    # 缓存相关的接口
    return [
        api.resp.post("/zdppy_cache", set),  # 设置缓存
        api.resp.get("/zdppy_cache", get),  # 获取缓存
        api.resp.get("/zdppy_cache/size", get_size),  # 获取缓存大小
        api.resp.delete("/zdppy_cache/all", delete_all),  # 清空缓存
        api.resp.get("/zdppy_caches", query),  # 查询缓存
        api.resp.delete("/zdppy_cache", delete),  # 删除缓存
        api.resp.delete("/zdppy_caches", resize),  # 清理缓存
    ]


def manage_cache(key1, key2, api):
    """
    生成管理缓存相关的接口
    :param key1: 管理员的第一个加密key
    :param key2: 管理员的第二个加密key
    :param api: zdppy_api 的包
    :return:
    """
    # 管理员的缓存对象
    admin_cache = UserCache(key1, key2)

    def get_cache(req):
        """获取缓存对象"""
        # 获取请求头参数
        ukey1 = api.req.get_header(req, "key1")
        ukey2 = api.req.get_header(req, "key2")
        username = api.req.get_header(req, "username")
        if ukey1 is None or ukey2 is None or username is None:
            return None, "key1或key2或username不能为空"

        # 管理员
        if ukey1 != key1 or ukey2 != key2:
            return None, "权限校验失败，您没有访问权限"

        # 缓存是否存在
        user_cache_dir = admin_cache.get(username)
        if not user_cache_dir:
            return None, "不存在该用户的缓存"

        # 返回用户缓存对象
        return Cache(user_cache_dir), None

    # 管理员
    async def set(req):
        """设置缓存的接口"""
        # 获取缓存对象
        cache_obj, err = get_cache(req)
        if err:
            return api.resp.error_400(err)

        # 设置缓存
        data = await api.req.get_json(req)
        key = data.get("key")
        value = data.get("value")
        expire = data.get("expire")
        if not expire:
            expire = 180
        cache_obj.set(key, value, expire)
        return api.resp.success()

    async def get(req):
        """获取缓存的接口"""
        # 获取缓存对象
        cache_obj, err = get_cache(req)
        if err is not None:
            return api.resp.error_400(err)

        # 获取key
        data = await api.req.get_json(req)
        key = data.get("key")

        # 获取缓存
        value = cache_obj.get(key)
        if not value:
            return api.resp.error_404()
        return api.resp.success({"key": key, "value": value})

    async def query(req):
        """查询缓存的接口"""
        # 获取缓存对象
        cache_obj, err = get_cache(req)
        if err is not None:
            return api.resp.error_400(err)

        # 获取查询参数
        params = await api.req.get_json(req)

        # 默认查询所有key
        data = cache_obj.get_all_keys(False)
        if params.get("error"):  # 什么参数都没有传
            return api.resp.success({
                "query": params,
                "data": data,
            })

        # 是否包含值
        has_value = params.get("value")
        # 是否返回详细信息
        has_detail = params.get("detail")
        # 是否只获取激活的
        has_active = params.get("active")
        if has_active:
            # 只查询未过期的
            if has_detail:
                data = cache_obj.get_all()
            elif has_value:
                data = cache_obj.get_all_items()
            else:
                data = cache_obj.get_all_keys()
        else:
            # 查询所有的
            if has_detail:
                data = cache_obj.get_all(False)
            elif has_value:
                data = cache_obj.get_all_items(False)
            else:
                data = cache_obj.get_all_keys(False)
        return api.resp.success({
            "query": params,
            "data": data,
        })

    async def delete(req):
        """删除缓存的接口"""
        # 获取缓存对象
        cache_obj, err = get_cache(req)
        if err is not None:
            return api.resp.error_400(err)

        # 获取查询参数
        data = await api.req.get_json(req)
        key = data.get("key")

        # 删除缓存
        cache_obj.delete(key)
        return api.resp.success()

    async def resize(req):
        """重置缓存"""
        # 获取缓存对象
        cache_obj, err = get_cache(req)
        if err is not None:
            return api.resp.error_400(err)

        # 删除前大小
        old_size = cache_obj.get_size()

        # 获取要保留的过期缓存个数
        json_data = await api.req.get_json(req)
        limit = json_data.get("limit")
        if not limit:
            limit = 1000
        # 删除过期的缓存
        cache_obj.resize(False, limit)
        new_size = cache_obj.get_size()

        # 返回
        data = {"old_size": old_size, "new_size": new_size}
        return api.resp.success(data)

    async def get_size(req):
        """获取缓存对象"""
        # 获取缓存对象
        cache_obj, err = get_cache(req)
        if err is not None:
            return api.resp.error_400(err)

        # 查询缓存大小
        size = cache_obj.get_size()
        return api.resp.success({"size": size})

    async def delete_all(req):
        """清空缓存"""
        # 获取缓存对象
        cache_obj, err = get_cache(req)
        if err is not None:
            return api.resp.error_400(err)
        # 删除所有缓存
        cache_obj.delete_all()
        return api.resp.success()

    # 缓存相关的接口
    return [
        api.resp.post("/zdppy_cache/manage", set),  # 通过管理员设置用户缓存
        api.resp.get("/zdppy_cache/manage", get),  # 通过管理员获取用户缓存
        api.resp.get("/zdppy_cache/manage/size", get_size),  # 通过管理员获取用户缓存大小
        api.resp.delete("/zdppy_cache/manage/all", delete_all),  # 通过管理员清空用户缓存
        api.resp.get("/zdppy_caches/manage", query),  # 通过管理员查询用户缓存
        api.resp.delete("/zdppy_cache/manage", delete),  # 通过管理员删除用户缓存
        api.resp.delete("/zdppy_caches/manage", resize),  # 通过管理员清理用户缓存
    ]
