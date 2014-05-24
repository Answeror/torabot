from nose.tools import assert_equal
from .... import make
from ....ut.bunch import bunchr
from ....core.mod import mod
from .. import name
from .const import URI_QUERY_RESULT


def check_changes(old, new, n):
    app = make()
    with app.app_context():
        changes = list(mod(name).changes(old, new))
        assert_equal(len(changes), n)


def test_uri_no_change():
    yield check_changes, bunchr(URI_QUERY_RESULT), bunchr(URI_QUERY_RESULT), 0


def test_feed_new_change():
    yield (
        check_changes,
        bunchr({
            'query': URI_QUERY_RESULT['query'],
            'data': {
                'entries': URI_QUERY_RESULT['data']['entries'][1:],
            },
        }),
        bunchr(URI_QUERY_RESULT),
        1
    )
