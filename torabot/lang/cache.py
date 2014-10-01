from asyncio import coroutine
from functools import wraps
from .local import local


def cache0(name):
    key = 'torabot:temp:cache:' + name

    def call(f):
        @coroutine
        @wraps(f)
        def g():
            if (yield from local.redis.exists(key)):
                value = yield from local.redis.get(key)
            else:
                value = f()
                yield from local.redis.set(key, value)
            return value
        return g
    return call
