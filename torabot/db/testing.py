from functools import wraps
from contextlib import contextmanager
import logbook
from asyncio import coroutine
from ..app import App
from .schema import create_all
from . import db


class SandboxFixture(object):

    def setup(self):
        self.log_handler = logbook.TestHandler()
        self.log_handler.push_thread()

        # Connect to the database and create the schema within a transaction
        self.engine = db.make_engine()
        self.connection = self.engine.connect()
        self.transaction = self.connection.begin()
        create_all(self.connection)

    def teardown(self):
        # Roll back the top level transaction and disconnect from the database
        self.transaction.rollback()
        self.connection.close()
        self.engine.dispose()

        self.log_handler.pop_thread()


@contextmanager
def sandbox():
    app = App(__name__)
    app.config.from_object(__name__)
    db.init_app(app)
    with app.app_context():
        fixture = SandboxFixture()
        fixture.setup()
        try:
            yield fixture.connection
        finally:
            fixture.teardown()


def with_sandbox(f):
    @wraps(f)
    def g(*args, **kargs):
        with sandbox() as conn:
            return f(conn, *args, **kargs)
    return g


def with_async_sandbox(f):
    @coroutine
    @wraps(f)
    def g(*args, **kargs):
        app = App(__name__)
        app.config.from_object(__name__)
        db.init_app(app)
        with app.app_context():
            fixture = SandboxFixture()
            fixture.setup()
            try:
                return (yield from f(fixture.connection, *args, **kargs))
            finally:
                fixture.teardown()
    return g
