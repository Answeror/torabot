from nose.tools import assert_equal
from .... import make
from ....ut.bunch import bunchr
from ....core.mod import mod
from .. import name
from .const import SEARCH_QUERY_RESULT


def test_query_changes():
    app = make()
    with app.app_context():
        r = SEARCH_QUERY_RESULT
        changes = list(mod(name).changes(
            bunchr(query=r['query'], posts=r['posts'][1:]),
            bunchr(query=r['query'], posts=r['posts'])
        ))
        assert_equal(len(changes), 1)
