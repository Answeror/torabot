from nose.tools import assert_equal
from ....ut.async_test_tools import with_event_loop
from ..jinja2 import Target
from .ut import make_fs_env
from . import TestSuite


class TestJinja2(TestSuite):

    @with_event_loop
    def test_jinja2(self):
        target = Target(make_fs_env())
        assert_equal((yield from target(
            template={'name': 'torabot/get.jinja2'},
            kargs={'value': {'foo': 'bar'}, 'key': 'foo'}
        )), '"bar"')
