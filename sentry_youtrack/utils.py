from hashlib import md5

from sentry.utils.cache import cache


def cache_this(timeout=60):
    def decorator(func):
        def wrapper(*args, **kwargs):
            def get_cache_key(*args, **kwargs):
                params = list(args) + list(kwargs.values())
                encodestr = "".join(map(str, params))
                return md5(encodestr.encode()).hexdigest()
            key = get_cache_key(func.__name__, *args, **kwargs)
            result = cache.get(key)
            if not result:
                result = func(*args, **kwargs)
                cache.set(key, result, timeout)
            return result
        return wrapper
    return decorator


def get_int(value, default=0):
    try:
        return int(value)
    except ValueError:
        return default
