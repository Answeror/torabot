from functools import partial
from redis import StrictRedis
from asyncio import wait_for, coroutine
import asyncio_redis
from flask import current_app
from .facade import Facade


class Redis(Facade):

    name = 'redis'

    def __init__(self):
        super().__init__()

        for name in [
            'get',
            'set',
            'exists',
            'expire',
            'start_subscribe',
            'publish'
        ]:
            @coroutine
            def async_func(name, *args, **kargs):
                impl = yield from self.async_impl
                return (yield from getattr(impl, name)(*args, **kargs))

            # use async interface by default
            setattr(self, name, partial(async_func, name))
            setattr(self, 'async_' + name, partial(async_func, name))

            def sync_func(name, *args, **kargs):
                return getattr(self.sync_impl, name)(*args, **kargs)

            setattr(self, 'sync_' + name, partial(sync_func, name))

    def init_app(self, app):
        super().init_app(app)

        if self.get_inited(app):
            return

        app.config.setdefault('TORABOT_REDIS_HOST', 'localhost')
        app.config.setdefault('TORABOT_REDIS_PORT', 6379)
        app.config.setdefault('TORABOT_REDIS_POOLSIZE', 32)
        self.set_inited(app)

    @property
    @coroutine
    def async_impl(self):
        if 'async_impl' not in self.state:
            self.state['async_impl'] = yield from wait_for(
                asyncio_redis.Pool.create(
                    host=current_app.config['TORABOT_REDIS_HOST'],
                    port=current_app.config['TORABOT_REDIS_PORT'],
                    poolsize=current_app.config['TORABOT_REDIS_POOLSIZE']
                ),
                timeout=1
            )
        return self.state['async_impl']

    @property
    def sync_impl(self):
        if 'sync_impl' not in self.state:
            self.state['sync_impl'] = StrictRedis(
                host=current_app.config['TORABOT_REDIS_HOST'],
                port=current_app.config['TORABOT_REDIS_PORT']
            )
        return self.state['sync_impl']


redis = Redis()


__all__ = ['redis', 'Redis']
