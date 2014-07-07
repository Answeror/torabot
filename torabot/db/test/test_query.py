from nose.tools import assert_equal, assert_is_not_none, assert_greater
from datetime import datetime, timedelta
from . import g
from ..notice import get_notices_bi_user_id, count_recent_notice_bi_user_id
from ..user import add_user, add_email_bi_user_id, activate_email_bi_id
from ..watch import watch
from ..query import (
    add_query,
    get_sorted_active_queries,
    get_need_sync_queries,
    set_next_sync_time,
    is_query_active_bi_id,
    del_query_bi_id,
    get_query_count,
    del_inactive_queries,
)
from ..change import add_one_query_changes, del_old_changes


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


def test_broadcast_non_main_email_not_activated():
    with g.connection.begin_nested() as trans:
        user_id = fake_add_users(g.connection)[0]
        email_text = 'answeror+foo@gmail.com'
        email_id = add_email_bi_user_id(
            g.connection,
            id=user_id,
            email=email_text,
            label=''
        )
        query_id = fake_add_queries(g.connection)[0]
        watch(g.connection, user_id=user_id, query_id=query_id, email_id=email_id)
        add_one_query_changes(g.connection, query_id, [{}])
        assert_equal(len(get_notices_bi_user_id(g.connection, user_id)), 0)
        trans.rollback()


def test_broadcast_non_main_email_activated():
    with g.connection.begin_nested() as trans:
        user_id = fake_add_users(g.connection)[0]
        email_text = 'answeror+foo@gmail.com'
        email_id = add_email_bi_user_id(
            g.connection,
            id=user_id,
            email=email_text,
            label=''
        )
        query_id = fake_add_queries(g.connection)[0]
        watch(g.connection, user_id=user_id, query_id=query_id, email_id=email_id)
        activate_email_bi_id(g.connection, email_id)
        add_one_query_changes(g.connection, query_id, [{}])
        assert_equal(get_notices_bi_user_id(g.connection, user_id)[0].email, email_text)
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


def test_get_need_sync_queries():
    with g.connection.begin_nested() as trans:
        user_id = fake_add_users(g.connection)[0]
        query_ids = fake_add_queries(g.connection)
        assert_greater(len(query_ids), 1)
        assert_equal(len(get_need_sync_queries(g.connection)), 0)
        assert not is_query_active_bi_id(g.connection, query_ids[0])
        watch(g.connection, user_id=user_id, query_id=query_ids[0])
        assert is_query_active_bi_id(g.connection, query_ids[0])
        assert_equal(len(get_need_sync_queries(g.connection)), 1)
        set_next_sync_time(g.connection, id=query_ids[1], time=datetime.utcnow() + timedelta(days=1))
        assert_equal(len(get_need_sync_queries(g.connection)), 1)
        set_next_sync_time(g.connection, id=query_ids[1], time=datetime.utcnow() - timedelta(days=1))
        assert_equal(len(get_need_sync_queries(g.connection)), 2)
        trans.rollback()


def test_count_recent_notice():
    with g.connection.begin_nested() as trans:
        user_id = fake_add_users(g.connection)[0]
        query_id = fake_add_queries(g.connection)[0]
        watch(g.connection, user_id=user_id, query_id=query_id)
        add_one_query_changes(g.connection, query_id, [{}])
        assert_equal(count_recent_notice_bi_user_id(
            g.connection,
            user_id,
            timedelta(days=1)
        ), 1)
        assert_equal(count_recent_notice_bi_user_id(
            g.connection,
            user_id,
            timedelta(days=0)
        ), 0)
        trans.rollback()


def test_query_delete_cascade():
    with g.connection.begin_nested() as trans:
        user_id = fake_add_users(g.connection)[0]
        query_id = fake_add_queries(g.connection)[0]
        watch(g.connection, user_id=user_id, query_id=query_id)
        add_one_query_changes(g.connection, query_id, [{}])
        del_query_bi_id(g.connection, query_id)
        assert_equal(len(get_notices_bi_user_id(g.connection, user_id)), 0)
        trans.rollback()


def test_del_inactive_queries():
    with g.connection.begin_nested() as trans:
        user_id = fake_add_users(g.connection)[0]
        query_id = fake_add_queries(g.connection)[0]
        watch(g.connection, user_id=user_id, query_id=query_id)
        del_inactive_queries(
            g.connection,
            before=datetime.utcnow(),
            limit=42
        )
        assert_equal(get_query_count(g.connection), 1)
        trans.rollback()


def test_del_inactive_queries_before():
    with g.connection.begin_nested() as trans:
        user_id = fake_add_users(g.connection)[0]
        query_id = fake_add_queries(g.connection)[0]
        watch(g.connection, user_id=user_id, query_id=query_id)
        del_inactive_queries(
            g.connection,
            before=datetime.utcnow() - timedelta(days=1),
            limit=42
        )
        assert_equal(get_query_count(g.connection), 2)
        trans.rollback()


def test_del_inactive_queries_limit():
    with g.connection.begin_nested() as trans:
        fake_add_queries(g.connection)
        del_inactive_queries(
            g.connection,
            before=datetime.utcnow(),
            limit=1
        )
        assert_equal(get_query_count(g.connection), 1)
        trans.rollback()


def test_del_old_changes():
    with g.connection.begin_nested() as trans:
        user_id = fake_add_users(g.connection)[0]
        query_id = fake_add_queries(g.connection)[0]
        watch(g.connection, user_id=user_id, query_id=query_id)
        add_one_query_changes(g.connection, query_id, [{}])
        del_old_changes(
            g.connection,
            before=datetime.utcnow(),
            limit=42
        )
        assert_equal(len(get_notices_bi_user_id(g.connection, user_id)), 0)
        trans.rollback()


def test_del_old_changes_before():
    with g.connection.begin_nested() as trans:
        user_id = fake_add_users(g.connection)[0]
        query_id = fake_add_queries(g.connection)[0]
        watch(g.connection, user_id=user_id, query_id=query_id)
        add_one_query_changes(g.connection, query_id, [{}])
        del_old_changes(
            g.connection,
            before=datetime.utcnow() - timedelta(days=1),
            limit=42
        )
        assert_equal(len(get_notices_bi_user_id(g.connection, user_id)), 1)
        trans.rollback()


def test_del_old_changes_limit():
    with g.connection.begin_nested() as trans:
        user_id = fake_add_users(g.connection)[0]
        query_id = fake_add_queries(g.connection)[0]
        watch(g.connection, user_id=user_id, query_id=query_id)
        add_one_query_changes(g.connection, query_id, [{}])
        add_one_query_changes(g.connection, query_id, [{}])
        del_old_changes(
            g.connection,
            before=datetime.utcnow(),
            limit=1
        )
        assert_equal(len(get_notices_bi_user_id(g.connection, user_id)), 1)
        trans.rollback()
