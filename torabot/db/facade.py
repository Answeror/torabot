import inspect
from functools import wraps
from flask import current_app, _app_ctx_stack as stack
from asyncio import coroutine, iscoroutine
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from threading import Lock
from ..ut.facade import Facade as Base


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
                    return (yield from self.run_in_executor(func, *args, **kargs))
                attrs[name] = async_func

        from . import errors
        for name in dir(errors):
            expcls = getattr(errors, name)
            if isinstance(expcls, type) and issubclass(expcls, Exception):
                attrs[name] = expcls

        return type.__new__(cls, name, bases, attrs)


class Facade(Base, metaclass=Meta):

    name = 'db'

    def __init__(self):
        super().__init__()
        self._engine_lock = Lock()

    def init_app(self, app):
        super().init_app(app)

        if self.get_inited(app):
            return

        app.config.setdefault(
            'TORABOT_TEST_CONNECTION_STRING',
            'postgresql+psycopg2://localhost/torabot-test'
        )
        app.teardown_appcontext(self.teardown)
        self.set_inited(app)

    def teardown(self, exception):
        ctx = stack.top
        db_session = getattr(ctx, 'db_session', None)
        if db_session is not None:
            db_session.close()

    def make_engine(self):
        from sqlalchemy import create_engine
        return create_engine(
            current_app.config['TORABOT_TEST_CONNECTION_STRING']
        )

    def connect(self, engine=None):
        if engine is None:
            engine = self.engine
        return engine.connect()

    @property
    def engine(self):
        with self._engine_lock:
            value = self.state.get('db_engine')
            if value is None:
                self.state.db_engine = value = self.make_engine()
            return value

    @property
    def bind(self):
        value = self.state.get('connection')
        if value:
            return value
        return self.engine

    @property
    def has_connection(self):
        return self.state.get('connection') is not None

    @property
    def session(self):
        value = self.state.get('session')
        if value:
            return value

        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'db_session'):
                ctx.db_session = self.make_session()
            return ctx.db_session

    @property
    def connection(self):
        return self.session.connection()

    def make_session(self, bind=None):
        if bind is None:
            bind = self.bind

        Session = sessionmaker(bind=bind)
        return Session()

    @contextmanager
    def connection_context(self, commit=False, bind=None):
        session = self.make_session(bind)
        try:
            yield ConnectionProxy(session)
            if commit and bind is self.bind and self.has_connection:
                session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def with_optional_bind(self, func):
        if iscoroutine(func):
            @coroutine
            @wraps(func)
            def wrapped(*args, **kargs):
                if 'bind' not in kargs:
                    kargs['bind'] = self.bind
                return (yield from func(*args, **kargs))
        else:
            @wraps(func)
            def wrapped(*args, **kargs):
                if 'bind' not in kargs:
                    kargs['bind'] = self.bind
                return func(*args, **kargs)
        return wrapped

    def with_optional_connection(self, *args, **kargs):
        def wrap(func):
            options = kargs.copy()
            if 'commit' not in options:
                options['commit'] = False
            return (
                self._with_optional_connection_async if iscoroutine(func)
                else self._with_optional_connection_sync
            )(func, **options)

        if len(args) == 1:
            if callable(args[0]):
                return wrap(args[0])
            raise TypeError('Argument 1 to @with_optional_connection() must be a callable')

        if args:
            raise TypeError(
                '@with_optional_connection() takes exactly 1 argument ({0} given)'.format(
                    sum([len(args), len(kargs)])
                )
            )

        return wrap

    def _with_optional_connection_async(self, func, commit):
        @coroutine
        @wraps(func)
        def wrapped(*args, **kargs):
            if 'conn' in kargs:
                return (yield from func(*args, **kargs))
            with self.connection_context(commit=commit) as conn:
                return (yield from func(*args, conn=conn, **kargs))
        return wrapped

    def _with_optional_connection_sync(self, func, commit):
        @wraps(func)
        def wrapped(*args, **kargs):
            if 'conn' in kargs:
                return func(*args, **kargs)
            with self.connection_context(commit=commit) as conn:
                return func(*args, conn=conn, **kargs)
        return wrapped

    @contextmanager
    def sandbox(self):
        from .schema import create_all

        self.state.connection = self.connect()
        try:
            transaction = self.state.connection.begin()
            create_all(self.state.connection)
            yield self.state.connection
        finally:
            transaction.rollback()
            self.state.connection.close()
            self.state.connection = None

    @property
    def SandboxTestSuiteMixin(self):
        from .testing import SandboxTestSuiteMixin
        return SandboxTestSuiteMixin


class ConnectionProxy(object):

    def __init__(self, session):
        self.session = session

    def __getattr__(self, name):
        return getattr(self.session.connection(), name)


__all__ = ['Facade']
