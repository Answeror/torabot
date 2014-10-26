from nose.tools import (
    assert_equal,
    assert_is_not_none,
    assert_greater,
    assert_raises,
    assert_is_none
)
from datetime import datetime, timedelta
from .. import operations as op
from .. import db
from . import TestSuite


def prepare_user(conn):
    user_id = op.add_user(
        conn,
        name='answeror',
        email='answeror+torabot@gmail.com',
        password_hash='whatever',
    )
    assert_is_not_none(user_id)
    return user_id


def fake_add_users(conn):
    user_ids = [op.add_user(
        conn,
        name=name,
        email='%s@gmail.com' % name,
        password_hash=name,
    ) for name in ['foo', 'bar']]
    for user_id in user_ids:
        op.activate_user_bi_id(conn, user_id)
    return user_ids


def fake_add_queries(conn):
    return [op.add_query(conn, kind='foo', text=name) for name in [
        '0' * 12,
        '1' * 12
    ]]


class TestOperations(db.SandboxTestSuiteMixin, TestSuite):

    def test_broadcast_one(self):
        user_id = fake_add_users(db.connection)[0]
        query_id = fake_add_queries(db.connection)[0]
        op.watch(db.connection, user_id=user_id, query_id=query_id)
        op.add_one_query_changes(db.connection, query_id, [{}])
        assert_equal(len(op.get_notices_bi_user_id(db.connection, user_id)), 1)

    def test_broadcast_non_main_email_not_activated(self):
        user_id = fake_add_users(db.connection)[0]
        email_text = 'answeror+foo@gmail.com'
        email_id = op.add_email_bi_user_id(
            db.connection,
            id=user_id,
            email=email_text,
            label=''
        )
        query_id = fake_add_queries(db.connection)[0]
        op.watch(db.connection, user_id=user_id, query_id=query_id, email_id=email_id)
        op.add_one_query_changes(db.connection, query_id, [{}])
        assert_equal(len(op.get_notices_bi_user_id(db.connection, user_id)), 0)

    def test_broadcast_non_main_email_activated(self):
        user_id = fake_add_users(db.connection)[0]
        email_text = 'answeror+foo@gmail.com'
        email_id = op.add_email_bi_user_id(
            db.connection,
            id=user_id,
            email=email_text,
            label=''
        )
        query_id = fake_add_queries(db.connection)[0]
        op.watch(db.connection, user_id=user_id, query_id=query_id, email_id=email_id)
        op.activate_email_bi_id(db.connection, email_id)
        op.add_one_query_changes(db.connection, query_id, [{}])
        assert_equal(op.get_notices_bi_user_id(db.connection, user_id)[0].email, email_text)

    def test_broadcast_twice(self):
        user_id = fake_add_users(db.connection)[0]
        query_id = fake_add_queries(db.connection)[0]
        op.add_one_query_changes(db.connection, query_id, [{}])
        op.watch(db.connection, user_id=user_id, query_id=query_id)
        assert_equal(len(op.get_notices_bi_user_id(db.connection, user_id)), 0)
        op.add_one_query_changes(db.connection, query_id, [{}])
        assert_equal(len(op.get_notices_bi_user_id(db.connection, user_id)), 1)

    def test_broadcast_two_users(self):
        user_ids = fake_add_users(db.connection)
        query_id = fake_add_queries(db.connection)[0]
        for user_id in user_ids:
            op.watch(db.connection, user_id=user_id, query_id=query_id)
        op.add_one_query_changes(db.connection, query_id, [{}])
        for user_id in user_ids:
            assert_equal(len(op.get_notices_bi_user_id(db.connection, user_id)), 1)

    def test_broadcast_two_changes_two_users(self):
        user_ids = fake_add_users(db.connection)
        query_id = fake_add_queries(db.connection)[0]
        for user_id in user_ids:
            op.watch(db.connection, user_id=user_id, query_id=query_id)
        op.add_one_query_changes(db.connection, query_id, [{}, {}])
        for user_id in user_ids:
            assert_equal(len(op.get_notices_bi_user_id(db.connection, user_id)), 2)

    def test_add_query(self):
        assert_is_not_none(op.add_query(db.connection, kind='bar', text='foo'))

    def test_get_sorted_active_queries(self):
        user_id = fake_add_users(db.connection)[0]
        query_ids = fake_add_queries(db.connection)
        op.watch(db.connection, user_id=user_id, query_id=query_ids[0])
        assert_greater(len(query_ids), 1)
        assert_equal(len(op.get_sorted_active_queries(db.connection)), 1)

    def test_get_need_sync_queries(self):
        user_id = fake_add_users(db.connection)[0]
        query_ids = fake_add_queries(db.connection)
        assert_greater(len(query_ids), 1)
        assert_equal(len(op.get_need_sync_queries(db.connection)), 0)
        assert not op.is_query_active_bi_id(db.connection, query_ids[0])
        op.watch(db.connection, user_id=user_id, query_id=query_ids[0])
        assert op.is_query_active_bi_id(db.connection, query_ids[0])
        assert_equal(len(op.get_need_sync_queries(db.connection)), 1)
        op.set_next_sync_time(db.connection, id=query_ids[1], time=datetime.utcnow() + timedelta(days=1))
        assert_equal(len(op.get_need_sync_queries(db.connection)), 1)
        op.set_next_sync_time(db.connection, id=query_ids[1], time=datetime.utcnow() - timedelta(days=1))
        assert_equal(len(op.get_need_sync_queries(db.connection)), 2)

    def test_count_recent_notice(self):
        user_id = fake_add_users(db.connection)[0]
        query_id = fake_add_queries(db.connection)[0]
        op.watch(db.connection, user_id=user_id, query_id=query_id)
        op.add_one_query_changes(db.connection, query_id, [{}])
        assert_equal(op.count_recent_notice_bi_user_id(
            db.connection,
            user_id,
            timedelta(days=1)
        ), 1)
        assert_equal(op.count_recent_notice_bi_user_id(
            db.connection,
            user_id,
            timedelta(days=0)
        ), 0)

    def test_query_delete_cascade(self):
        user_id = fake_add_users(db.connection)[0]
        query_id = fake_add_queries(db.connection)[0]
        op.watch(db.connection, user_id=user_id, query_id=query_id)
        op.add_one_query_changes(db.connection, query_id, [{}])
        op.del_query_bi_id(db.connection, query_id)
        assert_equal(len(op.get_notices_bi_user_id(db.connection, user_id)), 0)

    def test_del_inactive_queries(self):
        user_id = fake_add_users(db.connection)[0]
        query_id = fake_add_queries(db.connection)[0]
        op.watch(db.connection, user_id=user_id, query_id=query_id)
        op.del_inactive_queries(
            db.connection,
            before=datetime.utcnow(),
            limit=42
        )
        assert_equal(op.get_query_count(db.connection), 1)

    def test_del_inactive_queries_before(self):
        user_id = fake_add_users(db.connection)[0]
        query_id = fake_add_queries(db.connection)[0]
        op.watch(db.connection, user_id=user_id, query_id=query_id)
        op.del_inactive_queries(
            db.connection,
            before=datetime.utcnow() - timedelta(days=1),
            limit=42
        )
        assert_equal(op.get_query_count(db.connection), 2)

    def test_del_inactive_queries_limit(self):
        fake_add_queries(db.connection)
        op.del_inactive_queries(
            db.connection,
            before=datetime.utcnow(),
            limit=1
        )
        assert_equal(op.get_query_count(db.connection), 1)

    def test_del_old_changes(self):
        user_id = fake_add_users(db.connection)[0]
        query_id = fake_add_queries(db.connection)[0]
        op.watch(db.connection, user_id=user_id, query_id=query_id)
        op.add_one_query_changes(db.connection, query_id, [{}])
        op.del_old_changes(
            db.connection,
            before=datetime.utcnow(),
            limit=42
        )
        assert_equal(len(op.get_notices_bi_user_id(db.connection, user_id)), 0)

    def test_del_old_changes_before(self):
        user_id = fake_add_users(db.connection)[0]
        query_id = fake_add_queries(db.connection)[0]
        op.watch(db.connection, user_id=user_id, query_id=query_id)
        op.add_one_query_changes(db.connection, query_id, [{}])
        op.del_old_changes(
            db.connection,
            before=datetime.utcnow() - timedelta(days=1),
            limit=42
        )
        assert_equal(len(op.get_notices_bi_user_id(db.connection, user_id)), 1)

    def test_del_old_changes_limit(self):
        user_id = fake_add_users(db.connection)[0]
        query_id = fake_add_queries(db.connection)[0]
        op.watch(db.connection, user_id=user_id, query_id=query_id)
        op.add_one_query_changes(db.connection, query_id, [{}])
        op.add_one_query_changes(db.connection, query_id, [{}])
        op.del_old_changes(
            db.connection,
            before=datetime.utcnow(),
            limit=1
        )
        assert_equal(len(op.get_notices_bi_user_id(db.connection, user_id)), 1)

    def test_add_changes_unique(self):
        query_id = fake_add_queries(db.connection)[0]
        assert_equal(op.get_change_count(db.connection), 0)
        op.add_one_query_changes(
            db.connection,
            query_id,
            [{}]
        )
        assert_equal(op.get_change_count(db.connection), 1)
        op.add_one_query_changes_unique(
            db.connection,
            query_id,
            [{}],
            timedelta(days=1)
        )
        assert_equal(op.get_change_count(db.connection), 1)
        op.add_one_query_changes_unique(
            db.connection,
            query_id,
            [{}],
            timedelta(days=-1)
        )
        assert_equal(op.get_change_count(db.connection), 2)

    def test_maxwatch(self):
        user_id = op.add_user(
            db.connection,
            name='answeror',
            email='answeror+torabot@gmail.com',
            password_hash='whatever',
        )

        query_ids = []
        for i in range(43):
            query_ids.append(op.add_query(
                db.connection,
                kind='foo',
                text=str(i)
            ))

        for query_id in query_ids[:-1]:
            op.watch(db.connection, user_id=user_id, query_id=query_id)

        assert_raises(
            db.WatchCountLimitError,
            op.watch,
            conn=db.connection,
            user_id=user_id,
            query_id=query_ids[-1]
        )

    def test_default_watch_email(self):
        user_id = op.add_user(
            db.connection,
            name='answeror',
            email='answeror+torabot@gmail.com',
            password_hash='whatever',
        )
        query_id = op.add_query(
            db.connection,
            kind='foo',
            text='bar',
        )
        op.watch(db.connection, user_id=user_id, query_id=query_id)
        watches = op.get_watches_bi_user_id(db.connection, user_id)
        assert_is_not_none(watches[0].email_id)
        assert_is_not_none(watches[0].email_text)

    def test_add_user(self):
        user_id = prepare_user(db.connection)
        user = op.get_user_detail_bi_id(db.connection, user_id)
        assert_equal(len(user.emails), 1)
        assert_equal(user.emails[0].label, 'main')

    def test_add_email(self):
        user_id = prepare_user(db.connection)
        op.add_email_bi_user_id(
            db.connection,
            id=user_id,
            email='answeror+foo@gmail.com',
            label=''
        )
        assert_equal(len(op.get_emails_bi_user_id(db.connection, user_id)), 2)

    def test_del_email(self):
        user_id = prepare_user(db.connection)
        email_id = op.add_email_bi_user_id(
            db.connection,
            id=user_id,
            email='answeror+foo@gmail.com',
            label=''
        )
        op.del_email_bi_id(db.connection, email_id)
        assert_equal(len(op.get_emails_bi_user_id(db.connection, user_id)), 1)

    def test_del_main_email_fail(self):
        user_id = prepare_user(db.connection)
        emails = op.get_emails_bi_user_id(db.connection, user_id)
        assert_raises(db.DeleteMainEmainError, op.del_email_bi_id, db.connection, emails[0].id)

    def test_update_main_email_id(self):
        user_id = prepare_user(db.connection)
        emails = op.get_emails_bi_user_id(db.connection, user_id)
        email, label = 'answeror+update@gmail.com', 'update'
        op.update_email_bi_id(
            db.connection,
            id=emails[0].id,
            email=email,
            label=label
        )
        user = op.get_user_detail_bi_id(db.connection, user_id)
        assert_equal(user.email, email)
        assert_equal(user.emails[0].text, email)
        assert_equal(user.emails[0].label, label)

    def test_update_non_main_email_id(self):
        user_id = prepare_user(db.connection)
        email_id = op.add_email_bi_user_id(
            db.connection,
            id=user_id,
            email='answeror+foo@gmail.com',
            label=''
        )
        email, label = 'answeror+update@gmail.com', 'update'
        op.update_email_bi_id(
            db.connection,
            id=email_id,
            email=email,
            label=label
        )
        user = op.get_user_detail_bi_id(db.connection, user_id)
        assert_equal(user.emails[-1].text, email)
        assert_equal(user.emails[-1].label, label)

    def test_activate_user(self):
        user_id = prepare_user(db.connection)
        op.activate_user_bi_id(db.connection, user_id)
        assert op.user_activated_bi_id(db.connection, user_id)
        emails = op.get_emails_bi_user_id(db.connection, user_id)
        assert emails[0].activated

    def test_inactivate_user(self):
        user_id = prepare_user(db.connection)
        op.activate_user_bi_id(db.connection, user_id)
        op.inactivate_user_bi_id(db.connection, user_id)
        assert not op.user_activated_bi_id(db.connection, user_id)
        emails = op.get_emails_bi_user_id(db.connection, user_id)
        assert not emails[0].activated

    def test_activate_main_email(self):
        user_id = prepare_user(db.connection)
        emails = op.get_emails_bi_user_id(db.connection, user_id)
        op.activate_email_bi_id(db.connection, emails[0].id)
        assert op.email_activated_bi_id(db.connection, emails[0].id)
        assert op.user_activated_bi_id(db.connection, user_id)

    def test_inactivate_main_email(self):
        user_id = prepare_user(db.connection)
        emails = op.get_emails_bi_user_id(db.connection, user_id)
        op.activate_email_bi_id(db.connection, emails[0].id)
        op.inactivate_email_bi_id(db.connection, emails[0].id)
        assert not op.email_activated_bi_id(db.connection, emails[0].id)
        assert not op.user_activated_bi_id(db.connection, user_id)

    def test_activate_non_main_email(self):
        user_id = prepare_user(db.connection)
        email_id = op.add_email_bi_user_id(
            db.connection,
            id=user_id,
            email='answeror+foo@gmail.com',
            label=''
        )
        op.activate_email_bi_id(db.connection, email_id)
        assert op.email_activated_bi_id(db.connection, email_id)

    def test_inactivate_non_main_email(self):
        user_id = prepare_user(db.connection)
        email_id = op.add_email_bi_user_id(
            db.connection,
            id=user_id,
            email='answeror+foo@gmail.com',
            label=''
        )
        op.activate_email_bi_id(db.connection, email_id)
        op.inactivate_email_bi_id(db.connection, email_id)
        assert not op.email_activated_bi_id(db.connection, email_id)

    def test_email_count_limit(self):
        user_id = prepare_user(db.connection)
        for i in range(2):
            op.add_email_bi_user_id(
                db.connection,
                id=user_id,
                email='answeror+%d@gmail.com' % i,
                label=''
            )
        assert_raises(
            db.EmailCountLimitError,
            op.add_email_bi_user_id,
            db.connection,
            id=user_id,
            email='answeror+fail@gmail.com',
            label=''
        )

    def test_set_password_hash_bi_email(self):
        prepare_user(db.connection)
        email = 'answeror+torabot@gmail.com'
        op.set_password_hash_bi_email(db.connection, email, 'new hash')
        assert_equal(
            op.get_password_hash_bi_email(db.connection, email),
            'new hash'
        )

    def test_get_user_id_bi_email(self):
        user_id = prepare_user(db.connection)
        assert_equal(
            op.get_user_id_bi_email(db.connection, 'answeror+torabot@gmail.com'),
            user_id
        )
        assert_is_none(
            op.get_user_id_bi_email(db.connection, 'noanswer@gmail.com')
        )

    def test_has_email(self):
        prepare_user(db.connection)
        assert op.has_email(db.connection, 'answeror+torabot@gmail.com')
        assert not op.has_email(db.connection, 'noanswer@gmail.com')
