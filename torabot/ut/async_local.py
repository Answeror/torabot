import asyncio_redis
from asyncio import coroutine
from .local import Local as SyncLocal


class AsyncLocal(object):

    def __init__(self, conf='toraconf'):
        self.sync_local = SyncLocal(conf)

    @property
    @coroutine
    def redis(self):
        value = getattr(self, '_redis', None)
        if value is None:
            self._redis = value = yield from asyncio_redis.Pool.create(
                host=self.conf.get('TORABOT_REDIS_HOST', 'localhost'),
                port=self.conf.get('TORABOT_REDIS_PORT', 6379),
                poolsize=self.conf.get('TORABOT_REDIS_POOLSIZE', 32)
            )
        return value

    @property
    def conf(self):
        return self.sync_local.conf


local = AsyncLocal()
