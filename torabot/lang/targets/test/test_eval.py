from ....ut.async_test_tools import with_event_loop
from .. import Target
from nose.tools import assert_equal
from .ut import make_fs_env
from . import TestSuite


class TestEval(TestSuite):

    @with_event_loop
    def test_eval(self):
        assert_equal(
            (yield from Target.run(
                make_fs_env(),
                {
                    '@eval': {'@json_decode': '{"@echo": "foo"}'}
                }
            )),
            "foo"
        )
