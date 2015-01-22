from nose.tools import assert_equal, assert_is_instance
from asyncio import coroutine
from functools import wraps, partial
from unittest.mock import patch
from ...ut.testing import app_test_suite
from ...ut.redis import redis
from ...app import App
from ...db import db
from .. import core


app = App(__name__)
app.config.from_object('torabot.ut.test_config')
core.init_app(app)


TestSuite = app_test_suite(app)


def get(name):
    from .mod import Mod
    assert_equal(name, 'tora')
    return Mod()


def with_fake_tora_mod(func):
    @coroutine
    @wraps(func)
    def wrapped(*args, **kargs):
        from ..modo import modo
        from .mod import Mod
        with patch.object(modo, 'get', get):
            assert_is_instance(modo.get('tora'), Mod)
            return (yield from func(*args, **kargs))
    return wrapped
