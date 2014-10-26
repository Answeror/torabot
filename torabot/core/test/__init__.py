from nose.tools import assert_equal, assert_is_instance
from asyncio import coroutine
from functools import wraps, partial
from unittest.mock import patch
from ...ut.testing import app_test_suite
from ...app import App
from ...db import db
from ...redis import redis
from .. import core


app = App(__name__)
app.config.from_object('torabot.ut.test_config')
db.init_app(app)
redis.init_app(app)
core.init_app(app)


TestSuite = app_test_suite(app)


def get(orig, name):
    from .mod import Mod
    assert_equal(name, 'tora')
    return Mod(orig)


def with_fake_tora_mod(func):
    @coroutine
    @wraps(func)
    def wrapped(*args, **kargs):
        from ..modo import modo
        from .mod import Mod
        with patch.object(modo, 'get', partial(get, modo.get('tora'))):
            assert_is_instance(modo.get('tora'), Mod)
            return (yield from func(*args, **kargs))
    return wrapped
