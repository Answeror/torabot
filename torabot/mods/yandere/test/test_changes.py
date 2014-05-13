from nose.tools import assert_equal
from .... import make
from ....ut.bunch import bunchr
from ....core.mod import mod
from .. import name
from .const import POSTS_URI_QUERY_RESULT


def test_posts_uri_no_change():
    app = make()
    with app.test_client():
        changes = list(mod(name).changes(
            bunchr(POSTS_URI_QUERY_RESULT),
            bunchr(POSTS_URI_QUERY_RESULT)
        ))
        assert_equal(len(changes), 0)


def test_posts_uri_new_change():
    app = make()
    with app.test_client():
        r = bunchr(POSTS_URI_QUERY_RESULT)
        changes = list(mod(name).changes(
            bunchr(query=r.query, posts=r.posts[1:]),
            r
        ))
        assert_equal(len(changes), 1)
