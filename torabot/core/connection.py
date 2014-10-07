from contextlib import contextmanager
from ..ut.connection import ccontext, appccontext
assert appccontext
from ..ut.engine import appengine
from ..ut.bunch import Bunch
from ..db import DatabaseFixture


@contextmanager
def autoccontext(commit=False, **kargs):
    connection = g.get('connection', None)
    if connection is not None:
        kargs.update(connection=connection)
    else:
        try:
            kargs.update(engine=appengine())
        except:
            from .local import get_current_conf
            kargs.update(config=get_current_conf())

    with ccontext(commit=commit, **kargs) as conn:
        yield conn


g = Bunch()


class ContextFixture(object):

    def __init__(self):
        self.database_fixture = DatabaseFixture()

    def setup(self):
        self.database_fixture.setup()
        g.connection = self.database_fixture.connection

    def teardown(self):
        g.connection = None
        self.database_fixture.teardown()
