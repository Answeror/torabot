from nose.tools import assert_equal
from .... import make
from ....ut.bunch import bunchr
from ....core.mod import mod
from .. import name
from .const import RSS_RESULT


def check_changes(old, new, n):
    app = make()
    with app.app_context():
        changes = list(mod(name).changes(old, new))
        assert_equal(len(changes), n)


def test_rss_no_change():
    yield check_changes, bunchr(RSS_RESULT), bunchr(RSS_RESULT), 0


def test_rss_new_change():
    yield (
        check_changes,
        bunchr(query=RSS_RESULT['query'], arts=RSS_RESULT['arts'][1:]),
        bunchr(RSS_RESULT),
        1
    )
