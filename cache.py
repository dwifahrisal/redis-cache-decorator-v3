import functools
import json
import redis

r = redis.Redis(decode_responses=True)


def cached(ttl=300):
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kw):
            key = fn.__name__ + ':' + str(args) + ':' + str(kw)
            hit = r.get(key)
            if hit:
                return json.loads(hit)
            result = fn(*args, **kw)
            r.setex(key, ttl, json.dumps(result))
            return result
        return wrapper
    return deco
