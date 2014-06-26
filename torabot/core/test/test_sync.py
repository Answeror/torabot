from nose.tools import assert_equal
from unittest.mock import patch
from ...db import get_query_count
from ..sync import sync
from ..backends.postgresql import PostgreSQL
from .mod import Mod
from . import g


def mod(kind):
    assert_equal(kind, 'tora')
    return Mod()


@patch('torabot.core.sync.mod', mod)
def test_sync():
    with g.connection.begin_nested() as trans:
        sync(
            kind='tora',
            text='大嘘',
            timeout=0,
            sync_interval=300,
            backend=PostgreSQL(conn=g.connection)
        )
        assert_equal(get_query_count(g.connection), 1)
        trans.rollback()
