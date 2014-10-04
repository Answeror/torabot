from ....ut.async_test_tools import with_event_loop
from .. import Target
from nose.tools import assert_equal
from .ut import make_fs_env


@with_event_loop
def test_eval():
    assert_equal(
        (yield from Target.run(
            make_fs_env(),
            {
                '@eval': {'@json_decode': '{"@echo": "foo"}'}
            }
        )),
        "foo"
    )
