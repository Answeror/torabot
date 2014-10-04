from nose.tools import assert_equal
from ..local import Local


def test_conf():
    local = Local('torabot.ut.test.fakeconf')
    assert_equal(local.conf['FOO'], 'bar')
