from logbook import Logger
from functools import wraps


log = Logger(__name__)


def wrap(f):
    @wraps(f)
    def inner(self, *args, **kargs):
        if self.redis is None:
            return
        return f(self, *args, **kargs)
    return inner


def _(key):
    return 'torabot:' + key


class Redis(object):

    def __init__(self):
        try:
            from redis import Redis as R
            self.redis = R()
        except:
            log.exception('redis init failed')
            self.redis = None
            pass

    @wrap
    def blpop(self, key, *args, **kargs):
        return self.redis.blpop(_(key), *args, **kargs)

    @wrap
    def rpush(self, key, *args, **kargs):
        return self.redis.rpush(_(key), *args, **kargs)

    @wrap
    def delete(self, key, *args, **kargs):
        return self.redis.delete(_(key), *args, **kargs)


redis = Redis()


__all__ = [
    'redis'
]
