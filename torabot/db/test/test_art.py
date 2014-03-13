from hashlib import md5
from nose.tools import assert_is_not_none, assert_equal
from . import g
from ..art import add_art, put_art
from ..change import (
    has_change,
    has_change_bi_art_id,
    change_count_bi_art_id,
)


def fake_add_art(conn):
    return add_art(
        conn,
        title='foo',
        author='bar',
        company='foobar',
        uri='http://tora.aip.io/foo',
        status='other',
        hash=md5(b'foo').hexdigest(),
    )


def test_add_art():
    with g.connection.begin_nested() as trans:
        assert not has_change(g.connection)
        art_id = fake_add_art(g.connection)
        assert_is_not_none(art_id)
        assert has_change_bi_art_id(g.connection, art_id)
        trans.rollback()


def test_put_art():
    with g.connection.begin_nested() as trans:
        assert not has_change(g.connection)
        art_id = fake_add_art(g.connection)
        put_art(g.connection, id=art_id, params=dict(status='reserve'))
        assert_equal(change_count_bi_art_id(g.connection, art_id), 2)
        trans.rollback()


def test_put_art_twice():
    with g.connection.begin_nested() as trans:
        assert not has_change(g.connection)
        art_id = fake_add_art(g.connection)
        put_art(g.connection, id=art_id, params=dict(status='reserve'))
        put_art(g.connection, id=art_id, params=dict(status='reserve'))
        assert_equal(change_count_bi_art_id(g.connection, art_id), 2)
        trans.rollback()


def test_put_art_reserve_other():
    with g.connection.begin_nested() as trans:
        assert not has_change(g.connection)
        art_id = fake_add_art(g.connection)
        put_art(g.connection, id=art_id, params=dict(status='reserve'))
        put_art(g.connection, id=art_id, params=dict(status='other'))
        assert_equal(change_count_bi_art_id(g.connection, art_id), 2)
        trans.rollback()
