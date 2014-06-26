from nose.tools import assert_equal, assert_greater
from unittest.mock import patch
from ... import db
from ..sync import sync
from ..notice import send_notice
from ..backends.postgresql import PostgreSQL
from . import g


def send_notice_email(conf, target, notice):
    assert_equal(target, 'answeror+foo@gmail.com')


@patch('torabot.core.notice.send_notice_email', send_notice_email)
def test_send_notice():
    with g.connection.begin_nested() as trans:
        query_id = db.add_query(g.connection, kind='tora', text='东方')
        user_id = db.add_user(
            g.connection,
            name='answeror',
            email='answerro@gmail.com',
            openid='foo'
        )
        email_id = db.add_email_bi_user_id(
            g.connection,
            id=user_id,
            email='answeror+foo@gmail.com',
            label=''
        )
        db.activate_email_bi_id(g.connection, email_id)
        db.watch(
            g.connection,
            user_id=user_id,
            query_id=query_id,
            email_id=email_id
        )
        sync(
            kind='tora',
            text='东方',
            timeout=60,
            sync_interval=300,
            backend=PostgreSQL(conn=g.connection)
        )
        notices = db.get_pending_notices(g.connection)
        assert_greater(len(notices), 0)
        for notice in notices:
            assert send_notice(
                conf={},
                notice=notice,
                conn=g.connection,
            )
        trans.rollback()
