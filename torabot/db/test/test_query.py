from nose.tools import assert_equal, assert_is_not_none, assert_greater
from . import g
from ..notice import get_notices_bi_user_id
from ..user import add_user
from ..watch import watch
from ..query import add_query, get_sorted_active_queries
from ..change import add_one_query_changes


def fake_add_users(conn):
    return [add_user(
        conn,
        name=name,
        email='%s@gmail.com' % name,
        openid=name,
    ) for name in ['foo', 'bar']]


def fake_add_queries(conn):
    return [add_query(conn, kind='foo', text=name) for name in [
        '0' * 12,
        '1' * 12
    ]]


def test_broadcast_one():
    with g.connection.begin_nested() as trans:
        user_id = fake_add_users(g.connection)[0]
        query_id = fake_add_queries(g.connection)[0]
        watch(g.connection, user_id=user_id, query_id=query_id)
        add_one_query_changes(g.connection, query_id, [{}])
        assert_equal(len(get_notices_bi_user_id(g.connection, user_id)), 1)
        trans.rollback()


def test_broadcast_twice():
    with g.connection.begin_nested() as trans:
        user_id = fake_add_users(g.connection)[0]
        query_id = fake_add_queries(g.connection)[0]
        add_one_query_changes(g.connection, query_id, [{}])
        watch(g.connection, user_id=user_id, query_id=query_id)
        assert_equal(len(get_notices_bi_user_id(g.connection, user_id)), 0)
        add_one_query_changes(g.connection, query_id, [{}])
        assert_equal(len(get_notices_bi_user_id(g.connection, user_id)), 1)
        trans.rollback()


def test_broadcast_two_users():
    with g.connection.begin_nested() as trans:
        user_ids = fake_add_users(g.connection)
        query_id = fake_add_queries(g.connection)[0]
        for user_id in user_ids:
            watch(g.connection, user_id=user_id, query_id=query_id)
        add_one_query_changes(g.connection, query_id, [{}])
        for user_id in user_ids:
            assert_equal(len(get_notices_bi_user_id(g.connection, user_id)), 1)
        trans.rollback()


def test_broadcast_two_changes_two_users():
    with g.connection.begin_nested() as trans:
        user_ids = fake_add_users(g.connection)
        query_id = fake_add_queries(g.connection)[0]
        for user_id in user_ids:
            watch(g.connection, user_id=user_id, query_id=query_id)
        add_one_query_changes(g.connection, query_id, [{}, {}])
        for user_id in user_ids:
            assert_equal(len(get_notices_bi_user_id(g.connection, user_id)), 2)
        trans.rollback()


def test_add_query():
    with g.connection.begin_nested() as trans:
        assert_is_not_none(add_query(g.connection, kind='bar', text='foo'))
        trans.rollback()


def test_get_sorted_active_queries():
    with g.connection.begin_nested() as trans:
        user_id = fake_add_users(g.connection)[0]
        query_ids = fake_add_queries(g.connection)
        watch(g.connection, user_id=user_id, query_id=query_ids[0])
        assert_greater(len(query_ids), 1)
        assert_equal(len(get_sorted_active_queries(g.connection)), 1)
        trans.rollback()
