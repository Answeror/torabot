from nose.tools import (
    assert_equal,
    assert_is_not_none,
    assert_greater,
    assert_raises,
    assert_is_none
)
from datetime import datetime, timedelta
from .. import operations as op
from ..testing import with_sandbox
from ..errors import (
    DeleteMainEmainError,
    EmailCountLimitError,
    WatchCountLimitError
)


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


@with_sandbox
def test_broadcast_one(conn):
    user_id = fake_add_users(conn)[0]
    query_id = fake_add_queries(conn)[0]
    op.watch(conn, user_id=user_id, query_id=query_id)
    op.add_one_query_changes(conn, query_id, [{}])
    assert_equal(len(op.get_notices_bi_user_id(conn, user_id)), 1)


@with_sandbox
def test_broadcast_non_main_email_not_activated(conn):
    user_id = fake_add_users(conn)[0]
    email_text = 'answeror+foo@gmail.com'
    email_id = op.add_email_bi_user_id(
        conn,
        id=user_id,
        email=email_text,
        label=''
    )
    query_id = fake_add_queries(conn)[0]
    op.watch(conn, user_id=user_id, query_id=query_id, email_id=email_id)
    op.add_one_query_changes(conn, query_id, [{}])
    assert_equal(len(op.get_notices_bi_user_id(conn, user_id)), 0)


@with_sandbox
def test_broadcast_non_main_email_activated(conn):
    user_id = fake_add_users(conn)[0]
    email_text = 'answeror+foo@gmail.com'
    email_id = op.add_email_bi_user_id(
        conn,
        id=user_id,
        email=email_text,
        label=''
    )
    query_id = fake_add_queries(conn)[0]
    op.watch(conn, user_id=user_id, query_id=query_id, email_id=email_id)
    op.activate_email_bi_id(conn, email_id)
    op.add_one_query_changes(conn, query_id, [{}])
    assert_equal(op.get_notices_bi_user_id(conn, user_id)[0].email, email_text)


@with_sandbox
def test_broadcast_twice(conn):
    user_id = fake_add_users(conn)[0]
    query_id = fake_add_queries(conn)[0]
    op.add_one_query_changes(conn, query_id, [{}])
    op.watch(conn, user_id=user_id, query_id=query_id)
    assert_equal(len(op.get_notices_bi_user_id(conn, user_id)), 0)
    op.add_one_query_changes(conn, query_id, [{}])
    assert_equal(len(op.get_notices_bi_user_id(conn, user_id)), 1)


@with_sandbox
def test_broadcast_two_users(conn):
    user_ids = fake_add_users(conn)
    query_id = fake_add_queries(conn)[0]
    for user_id in user_ids:
        op.watch(conn, user_id=user_id, query_id=query_id)
    op.add_one_query_changes(conn, query_id, [{}])
    for user_id in user_ids:
        assert_equal(len(op.get_notices_bi_user_id(conn, user_id)), 1)


@with_sandbox
def test_broadcast_two_changes_two_users(conn):
    user_ids = fake_add_users(conn)
    query_id = fake_add_queries(conn)[0]
    for user_id in user_ids:
        op.watch(conn, user_id=user_id, query_id=query_id)
    op.add_one_query_changes(conn, query_id, [{}, {}])
    for user_id in user_ids:
        assert_equal(len(op.get_notices_bi_user_id(conn, user_id)), 2)


@with_sandbox
def test_add_query(conn):
    assert_is_not_none(op.add_query(conn, kind='bar', text='foo'))


@with_sandbox
def test_get_sorted_active_queries(conn):
    user_id = fake_add_users(conn)[0]
    query_ids = fake_add_queries(conn)
    op.watch(conn, user_id=user_id, query_id=query_ids[0])
    assert_greater(len(query_ids), 1)
    assert_equal(len(op.get_sorted_active_queries(conn)), 1)


@with_sandbox
def test_get_need_sync_queries(conn):
    user_id = fake_add_users(conn)[0]
    query_ids = fake_add_queries(conn)
    assert_greater(len(query_ids), 1)
    assert_equal(len(op.get_need_sync_queries(conn)), 0)
    assert not op.is_query_active_bi_id(conn, query_ids[0])
    op.watch(conn, user_id=user_id, query_id=query_ids[0])
    assert op.is_query_active_bi_id(conn, query_ids[0])
    assert_equal(len(op.get_need_sync_queries(conn)), 1)
    op.set_next_sync_time(conn, id=query_ids[1], time=datetime.utcnow() + timedelta(days=1))
    assert_equal(len(op.get_need_sync_queries(conn)), 1)
    op.set_next_sync_time(conn, id=query_ids[1], time=datetime.utcnow() - timedelta(days=1))
    assert_equal(len(op.get_need_sync_queries(conn)), 2)


@with_sandbox
def test_count_recent_notice(conn):
    user_id = fake_add_users(conn)[0]
    query_id = fake_add_queries(conn)[0]
    op.watch(conn, user_id=user_id, query_id=query_id)
    op.add_one_query_changes(conn, query_id, [{}])
    assert_equal(op.count_recent_notice_bi_user_id(
        conn,
        user_id,
        timedelta(days=1)
    ), 1)
    assert_equal(op.count_recent_notice_bi_user_id(
        conn,
        user_id,
        timedelta(days=0)
    ), 0)


@with_sandbox
def test_query_delete_cascade(conn):
    user_id = fake_add_users(conn)[0]
    query_id = fake_add_queries(conn)[0]
    op.watch(conn, user_id=user_id, query_id=query_id)
    op.add_one_query_changes(conn, query_id, [{}])
    op.del_query_bi_id(conn, query_id)
    assert_equal(len(op.get_notices_bi_user_id(conn, user_id)), 0)


@with_sandbox
def test_del_inactive_queries(conn):
    user_id = fake_add_users(conn)[0]
    query_id = fake_add_queries(conn)[0]
    op.watch(conn, user_id=user_id, query_id=query_id)
    op.del_inactive_queries(
        conn,
        before=datetime.utcnow(),
        limit=42
    )
    assert_equal(op.get_query_count(conn), 1)


@with_sandbox
def test_del_inactive_queries_before(conn):
    user_id = fake_add_users(conn)[0]
    query_id = fake_add_queries(conn)[0]
    op.watch(conn, user_id=user_id, query_id=query_id)
    op.del_inactive_queries(
        conn,
        before=datetime.utcnow() - timedelta(days=1),
        limit=42
    )
    assert_equal(op.get_query_count(conn), 2)


@with_sandbox
def test_del_inactive_queries_limit(conn):
    fake_add_queries(conn)
    op.del_inactive_queries(
        conn,
        before=datetime.utcnow(),
        limit=1
    )
    assert_equal(op.get_query_count(conn), 1)


@with_sandbox
def test_del_old_changes(conn):
    user_id = fake_add_users(conn)[0]
    query_id = fake_add_queries(conn)[0]
    op.watch(conn, user_id=user_id, query_id=query_id)
    op.add_one_query_changes(conn, query_id, [{}])
    op.del_old_changes(
        conn,
        before=datetime.utcnow(),
        limit=42
    )
    assert_equal(len(op.get_notices_bi_user_id(conn, user_id)), 0)


@with_sandbox
def test_del_old_changes_before(conn):
    user_id = fake_add_users(conn)[0]
    query_id = fake_add_queries(conn)[0]
    op.watch(conn, user_id=user_id, query_id=query_id)
    op.add_one_query_changes(conn, query_id, [{}])
    op.del_old_changes(
        conn,
        before=datetime.utcnow() - timedelta(days=1),
        limit=42
    )
    assert_equal(len(op.get_notices_bi_user_id(conn, user_id)), 1)


@with_sandbox
def test_del_old_changes_limit(conn):
    user_id = fake_add_users(conn)[0]
    query_id = fake_add_queries(conn)[0]
    op.watch(conn, user_id=user_id, query_id=query_id)
    op.add_one_query_changes(conn, query_id, [{}])
    op.add_one_query_changes(conn, query_id, [{}])
    op.del_old_changes(
        conn,
        before=datetime.utcnow(),
        limit=1
    )
    assert_equal(len(op.get_notices_bi_user_id(conn, user_id)), 1)


@with_sandbox
def test_add_changes_unique(conn):
    query_id = fake_add_queries(conn)[0]
    assert_equal(op.get_change_count(conn), 0)
    op.add_one_query_changes(
        conn,
        query_id,
        [{}]
    )
    assert_equal(op.get_change_count(conn), 1)
    op.add_one_query_changes_unique(
        conn,
        query_id,
        [{}],
        timedelta(days=1)
    )
    assert_equal(op.get_change_count(conn), 1)
    op.add_one_query_changes_unique(
        conn,
        query_id,
        [{}],
        timedelta(days=-1)
    )
    assert_equal(op.get_change_count(conn), 2)


@with_sandbox
def test_maxwatch(conn):
    user_id = op.add_user(
        conn,
        name='answeror',
        email='answeror+torabot@gmail.com',
        password_hash='whatever',
    )

    query_ids = []
    for i in range(43):
        query_ids.append(op.add_query(
            conn,
            kind='foo',
            text=str(i)
        ))

    for query_id in query_ids[:-1]:
        op.watch(conn, user_id=user_id, query_id=query_id)

    assert_raises(
        WatchCountLimitError,
        op.watch,
        conn=conn,
        user_id=user_id,
        query_id=query_ids[-1]
    )


@with_sandbox
def test_default_watch_email(conn):
    user_id = op.add_user(
        conn,
        name='answeror',
        email='answeror+torabot@gmail.com',
        password_hash='whatever',
    )
    query_id = op.add_query(
        conn,
        kind='foo',
        text='bar',
    )
    op.watch(conn, user_id=user_id, query_id=query_id)
    watches = op.get_watches_bi_user_id(conn, user_id)
    assert_is_not_none(watches[0].email_id)
    assert_is_not_none(watches[0].email_text)


@with_sandbox
def test_add_user(conn):
    user_id = prepare_user(conn)
    user = op.get_user_detail_bi_id(conn, user_id)
    assert_equal(len(user.emails), 1)
    assert_equal(user.emails[0].label, 'main')


@with_sandbox
def test_add_email(conn):
    user_id = prepare_user(conn)
    op.add_email_bi_user_id(
        conn,
        id=user_id,
        email='answeror+foo@gmail.com',
        label=''
    )
    assert_equal(len(op.get_emails_bi_user_id(conn, user_id)), 2)


@with_sandbox
def test_del_email(conn):
    user_id = prepare_user(conn)
    email_id = op.add_email_bi_user_id(
        conn,
        id=user_id,
        email='answeror+foo@gmail.com',
        label=''
    )
    op.del_email_bi_id(conn, email_id)
    assert_equal(len(op.get_emails_bi_user_id(conn, user_id)), 1)


@with_sandbox
def test_del_main_email_fail(conn):
    user_id = prepare_user(conn)
    emails = op.get_emails_bi_user_id(conn, user_id)
    assert_raises(DeleteMainEmainError, op.del_email_bi_id, conn, emails[0].id)


@with_sandbox
def test_update_main_email_id(conn):
    user_id = prepare_user(conn)
    emails = op.get_emails_bi_user_id(conn, user_id)
    email, label = 'answeror+update@gmail.com', 'update'
    op.update_email_bi_id(
        conn,
        id=emails[0].id,
        email=email,
        label=label
    )
    user = op.get_user_detail_bi_id(conn, user_id)
    assert_equal(user.email, email)
    assert_equal(user.emails[0].text, email)
    assert_equal(user.emails[0].label, label)


@with_sandbox
def test_update_non_main_email_id(conn):
    user_id = prepare_user(conn)
    email_id = op.add_email_bi_user_id(
        conn,
        id=user_id,
        email='answeror+foo@gmail.com',
        label=''
    )
    email, label = 'answeror+update@gmail.com', 'update'
    op.update_email_bi_id(
        conn,
        id=email_id,
        email=email,
        label=label
    )
    user = op.get_user_detail_bi_id(conn, user_id)
    assert_equal(user.emails[-1].text, email)
    assert_equal(user.emails[-1].label, label)


@with_sandbox
def test_activate_user(conn):
    user_id = prepare_user(conn)
    op.activate_user_bi_id(conn, user_id)
    assert op.user_activated_bi_id(conn, user_id)
    emails = op.get_emails_bi_user_id(conn, user_id)
    assert emails[0].activated


@with_sandbox
def test_inactivate_user(conn):
    user_id = prepare_user(conn)
    op.activate_user_bi_id(conn, user_id)
    op.inactivate_user_bi_id(conn, user_id)
    assert not op.user_activated_bi_id(conn, user_id)
    emails = op.get_emails_bi_user_id(conn, user_id)
    assert not emails[0].activated


@with_sandbox
def test_activate_main_email(conn):
    user_id = prepare_user(conn)
    emails = op.get_emails_bi_user_id(conn, user_id)
    op.activate_email_bi_id(conn, emails[0].id)
    assert op.email_activated_bi_id(conn, emails[0].id)
    assert op.user_activated_bi_id(conn, user_id)


@with_sandbox
def test_inactivate_main_email(conn):
    user_id = prepare_user(conn)
    emails = op.get_emails_bi_user_id(conn, user_id)
    op.activate_email_bi_id(conn, emails[0].id)
    op.inactivate_email_bi_id(conn, emails[0].id)
    assert not op.email_activated_bi_id(conn, emails[0].id)
    assert not op.user_activated_bi_id(conn, user_id)


@with_sandbox
def test_activate_non_main_email(conn):
    user_id = prepare_user(conn)
    email_id = op.add_email_bi_user_id(
        conn,
        id=user_id,
        email='answeror+foo@gmail.com',
        label=''
    )
    op.activate_email_bi_id(conn, email_id)
    assert op.email_activated_bi_id(conn, email_id)


@with_sandbox
def test_inactivate_non_main_email(conn):
    user_id = prepare_user(conn)
    email_id = op.add_email_bi_user_id(
        conn,
        id=user_id,
        email='answeror+foo@gmail.com',
        label=''
    )
    op.activate_email_bi_id(conn, email_id)
    op.inactivate_email_bi_id(conn, email_id)
    assert not op.email_activated_bi_id(conn, email_id)


@with_sandbox
def test_email_count_limit(conn):
    user_id = prepare_user(conn)
    for i in range(2):
        op.add_email_bi_user_id(
            conn,
            id=user_id,
            email='answeror+%d@gmail.com' % i,
            label=''
        )
    assert_raises(
        EmailCountLimitError,
        op.add_email_bi_user_id,
        conn,
        id=user_id,
        email='answeror+fail@gmail.com',
        label=''
    )


@with_sandbox
def test_set_password_hash_bi_email(conn):
    prepare_user(conn)
    email = 'answeror+torabot@gmail.com'
    op.set_password_hash_bi_email(conn, email, 'new hash')
    assert_equal(
        op.get_password_hash_bi_email(conn, email),
        'new hash'
    )


@with_sandbox
def test_get_user_id_bi_email(conn):
    user_id = prepare_user(conn)
    assert_equal(
        op.get_user_id_bi_email(conn, 'answeror+torabot@gmail.com'),
        user_id
    )
    assert_is_none(
        op.get_user_id_bi_email(conn, 'noanswer@gmail.com')
    )


@with_sandbox
def test_has_email(conn):
    prepare_user(conn)
    assert op.has_email(conn, 'answeror+torabot@gmail.com')
    assert not op.has_email(conn, 'noanswer@gmail.com')
