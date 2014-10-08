from nose.tools import assert_raises, assert_is_not_none
from .. import (
    add_user,
    watch,
    get_watches_bi_user_id,
    add_query,
    WatchCountLimitError
)
from . import g


def test_maxwatch():
    with g.connection.begin_nested() as trans:
        user_id = add_user(
            g.connection,
            name='answeror',
            email='answeror+torabot@gmail.com',
            password_hash='whatever',
        )

        query_ids = []
        for i in range(43):
            query_ids.append(add_query(
                g.connection,
                kind='foo',
                text=str(i)
            ))

        for query_id in query_ids[:-1]:
            watch(g.connection, user_id=user_id, query_id=query_id)

        assert_raises(
            WatchCountLimitError,
            watch,
            conn=g.connection,
            user_id=user_id,
            query_id=query_ids[-1]
        )
        trans.rollback()


def test_default_watch_email():
    with g.connection.begin_nested() as trans:
        user_id = add_user(
            g.connection,
            name='answeror',
            email='answeror+torabot@gmail.com',
            password_hash='whatever',
        )
        query_id = add_query(
            g.connection,
            kind='foo',
            text='bar',
        )
        watch(g.connection, user_id=user_id, query_id=query_id)
        watches = get_watches_bi_user_id(g.connection, user_id)
        assert_is_not_none(watches[0].email_id)
        assert_is_not_none(watches[0].email_text)
        trans.rollback()
