import json
from nose.tools import assert_equal
from ....ut.async_test_tools import with_event_loop
from .. import Target
from .ut import make_fs_env, read
from . import TestSuite


class TestJs(TestSuite):

    @with_event_loop
    def test_pixiv(self):
        result = yield from Target.run(
            make_fs_env(),
            json.loads(read('changes.json'))
        )
        assert_equal(result, ['c', 'd'])
