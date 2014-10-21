import inspect
from functools import wraps, partial
from flask import current_app, _app_ctx_stack as stack
from asyncio import coroutine
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor


class Meta(type):

    def __new__(cls, name, bases, attrs):
        from . import operations as op
        for name in dir(op):
            func = getattr(op, name)
            if (
                inspect.isfunction(func) and
                len(inspect.getargspec(func).args) > 0 and
                inspect.getargspec(func).args[0] == 'conn'
            ):
                @coroutine
                @wraps(func)
                def async_func(self, *args, func=func, **kargs):
                    return (yield from self._run_in_executor(func, *args, **kargs))
                attrs[name] = async_func
        return type.__new__(cls, name, bases, attrs)


class Facade(metaclass=Meta):

    def init_app(self, app):
        app.config.setdefault(
            'TORABOT_TEST_CONNECTION_STRING',
            'postgresql+psycopg2://localhost/torabot-test'
        )
        app.config.setdefault(
            'TORABOT_DB_CONCURRENCY',
            2 * cpu_count()
        )

    def make_engine(self):
        from sqlalchemy import create_engine
        return create_engine(
            current_app.config['TORABOT_TEST_CONNECTION_STRING']
        )

    @property
    def engine(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'engine'):
                ctx.engine = self.make_engine()
            return ctx.engine

    @property
    def executor(self):
        value = getattr(self, '_executor', None)
        if value is None:
            self._executor = value = ThreadPoolExecutor(
                max_workers=current_app.config['TORABOT_DB_CONCURRENCY']
            )
        return value

    @coroutine
    def _run_in_executor(self, func, *args, **kargs):
        return (yield from current_app.loop.run_in_executor(
            self.executor,
            partial(func, *args, **kargs)
        ))
