import aioredis
from flask import current_app
from asyncio import coroutine


class Local(object):

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
        return current_app.config


local = Local()
