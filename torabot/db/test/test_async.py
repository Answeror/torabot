from asyncio import coroutine, gather
from nose.tools import assert_equal
from ...ut.async_test_tools import with_event_loop
from .. import db
from . import TestSuite


@coroutine
def fake_add_users(conn):
    user_ids = []
    for name in ['foo', 'bar']:
        user_ids.append((yield from db.add_user(
            conn,
            name=name,
            email='%s@gmail.com' % name,
            password_hash=name,
        )))
    for user_id in user_ids:
        yield from db.activate_user_bi_id(conn, user_id)
    return user_ids


@coroutine
def fake_add_queries(conn):
    return (yield from gather(*[
        db.add_query(conn, kind='foo', text=name)
        for name in ['0' * 12, '1' * 12]
    ]))


class TestAsync(db.SandboxTestSuiteMixin, TestSuite):

    @with_event_loop
    def test_broadcast_one(self):
        user_id = (yield from fake_add_users(db.connection))[0]
        query_id = (yield from fake_add_queries(db.connection))[0]
        yield from db.watch(db.connection, user_id=user_id, query_id=query_id)
        yield from db.add_one_query_changes(db.connection, query_id, [{}])
        assert_equal(
            len((yield from db.get_notices_bi_user_id(db.connection, user_id))),
            1
        )
