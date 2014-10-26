from asyncio import wait_for
import asyncio_redis
from .ut.facade import Facade


class Redis(Facade):

    name = 'redis'

    def init_app(self, app):
        super().init_app(app)

        app.config.setdefault('TORABOT_REDIS_HOST', 'localhost')
        app.config.setdefault('TORABOT_REDIS_PORT', 6379)
        app.config.setdefault('TORABOT_REDIS_POOLSIZE', 32)

    @property
    def impl(self):
        if 'impl' not in self.state:
            self.state['impl'] = app.loop.run_until_complete(wait_for(
                asyncio_redis.Pool.create(
                    host=app.config['TORABOT_REDIS_HOST'],
                    port=app.config['TORABOT_REDIS_PORT'],
                    poolsize=app.config['TORABOT_REDIS_POOLSIZE']
                ),
                timeout=1
            ))
        return self.state['impl']

    def __getattr__(self, name):
        return getattr(self.impl, name)


redis = Redis()


__all__ = ['redis', 'Redis']
