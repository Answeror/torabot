from nose.tools import assert_equal
from unittest.mock import patch
from ...db import query_count
from ..sync import sync
from .mod import Mod
from . import g


def mod(kind):
    assert_equal(kind, 'tora')
    return Mod()


@patch('torabot.core.sync.mod', mod)
def test_sync():
    with g.connection.begin_nested() as trans:
        sync(g.connection, 'tora', '大嘘', 0)
        assert_equal(query_count(g.connection), 1)
        trans.rollback()
