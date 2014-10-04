import aioredis
from asyncio import coroutine
from .local import Local as SyncLocal


class AsyncLocal(object):

    def __init__(self, conf='toraconf'):
        self.sync_local = SyncLocal(conf)

    @property
    @coroutine
    def redis(self):
        value = getattr(self, '_redis')
        if value is None:
            self._redis = value = aioredis.create_redis(
                self.conf['TORABOT_REDIS_ADDRESS']
            )
        return value

    @property
    def conf(self):
        return self.sync_local.conf


local = AsyncLocal()
