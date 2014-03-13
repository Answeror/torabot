from hashlib import md5
from nose.tools import assert_equal, assert_is_not_none
from . import g
from ..notice import get_notice_bi_user_id
from ..user import add_user
from ..watch import watch
from ..art import add_art, put_art
from ..query import (
    add_query,
    add_result,
    set_results,
    add_results,
    del_results,
    result_count_bi_query_id,
)


def fake_add_users(conn):
    return [add_user(
        conn,
        name=name,
        email='%s@gmail.com' % name,
        openid=name,
    ) for name in ['foo', 'bar']]


def fake_add_arts(conn):
    return [add_art(
        conn,
        title=toraid,
        author=toraid,
        company=toraid,
        toraid=toraid,
        status='other',
        hash=md5(toraid.encode('ascii')).hexdigest(),
    ) for toraid in ['0' * 12, '1' * 12]]


def fake_add_queries(conn):
    return [add_query(conn, text=toraid) for toraid in [
        '0' * 12,
        '1' * 12
    ]]


def test_broadcast_one():
    with g.connection.begin_nested() as trans:
        user_id = fake_add_users(g.connection)[0]
        query_id = fake_add_queries(g.connection)[0]
        watch(g.connection, user_id=user_id, query_id=query_id)
        art_id = fake_add_arts(g.connection)[0]
        set_results(g.connection, query_id=query_id, art_ids=[art_id])
        assert_equal(len(get_notice_bi_user_id(g.connection, user_id)), 1)
        trans.rollback()


def test_broadcast_twice():
    with g.connection.begin_nested() as trans:
        user_id = fake_add_users(g.connection)[0]
        query_id = fake_add_queries(g.connection)[0]
        art_ids = fake_add_arts(g.connection)
        set_results(g.connection, query_id=query_id, art_ids=[art_ids[0]])
        watch(g.connection, user_id=user_id, query_id=query_id)
        assert_equal(len(get_notice_bi_user_id(g.connection, user_id)), 0)
        add_results(g.connection, query_id=query_id, ranks=[(art_ids[1], 1)])
        assert_equal(len(get_notice_bi_user_id(g.connection, user_id)), 1)
        trans.rollback()


def test_broadcast_update():
    with g.connection.begin_nested() as trans:
        user_id = fake_add_users(g.connection)[0]
        query_id = fake_add_queries(g.connection)[0]
        watch(g.connection, user_id=user_id, query_id=query_id)
        art_id = fake_add_arts(g.connection)[0]
        put_art(g.connection, id=art_id, status='reserve')
        set_results(g.connection, query_id=query_id, art_ids=[art_id])
        assert_equal(len(get_notice_bi_user_id(g.connection, user_id)), 2)
        trans.rollback()


def test_broadcast_dup():
    with g.connection.begin_nested() as trans:
        user_id = fake_add_users(g.connection)[0]
        query_ids = fake_add_queries(g.connection)
        for query_id in query_ids:
            watch(g.connection, user_id=user_id, query_id=query_id)
        art_id = fake_add_arts(g.connection)[0]
        for query_id in query_ids:
            set_results(g.connection, query_id=query_id, art_ids=[art_id])
        assert_equal(len(get_notice_bi_user_id(g.connection, user_id)), 1)
        trans.rollback()


def test_broadcast_two_users():
    with g.connection.begin_nested() as trans:
        user_ids = fake_add_users(g.connection)
        query_id = fake_add_queries(g.connection)[0]
        for user_id in user_ids:
            watch(g.connection, user_id=user_id, query_id=query_id)
        art_id = fake_add_arts(g.connection)[0]
        set_results(g.connection, query_id=query_id, art_ids=[art_id])
        for user_id in user_ids:
            assert_equal(len(get_notice_bi_user_id(g.connection, user_id)), 1)
        trans.rollback()


def test_broadcast_two_arts_two_users():
    with g.connection.begin_nested() as trans:
        user_ids = fake_add_users(g.connection)
        query_id = fake_add_queries(g.connection)[0]
        for user_id in user_ids:
            watch(g.connection, user_id=user_id, query_id=query_id)
        art_ids = fake_add_arts(g.connection)
        set_results(g.connection, query_id=query_id, art_ids=art_ids)
        for user_id in user_ids:
            assert_equal(len(get_notice_bi_user_id(g.connection, user_id)), 2)
        trans.rollback()


def test_add_query():
    with g.connection.begin_nested() as trans:
        assert_is_not_none(add_query(g.connection, text='foo'))
        trans.rollback()


def test_add_result():
    with g.connection.begin_nested() as trans:
        query_id = fake_add_queries(g.connection)[0]
        art_id = fake_add_arts(g.connection)[0]
        assert_is_not_none(add_result(
            g.connection,
            query_id=query_id,
            art_id=art_id,
            rank=0,
        ))
        trans.rollback()


def test_del_results():
    with g.connection.begin_nested() as trans:
        user_id = fake_add_users(g.connection)[0]
        query_id = fake_add_queries(g.connection)[0]
        watch(g.connection, user_id=user_id, query_id=query_id)
        art_ids = fake_add_arts(g.connection)
        add_results(
            g.connection,
            query_id=query_id,
            ranks=[(art_id, rank) for rank, art_id in enumerate(art_ids)],
        )
        del_results(g.connection, query_id)
        assert_equal(result_count_bi_query_id(g.connection, query_id), 0)
        trans.rollback()
