from nose.tools import (
    assert_is_not_none,
    assert_equal,
    assert_raises,
    assert_is_none
)
from .. import operations as op
from .. import (
    add_user,
    get_user_detail_bi_id,
    get_emails_bi_user_id,
    add_email_bi_user_id,
    del_email_bi_id,
    activate_user_bi_id,
    user_activated_bi_id,
    inactivate_user_bi_id,
    activate_email_bi_id,
    inactivate_email_bi_id,
    email_activated_bi_id,
    update_email_bi_id,
    DeleteMainEmainError,
    EmailCountLimitError
)
from . import g


def prepare_user(conn):
    user_id = add_user(
        conn,
        name='answeror',
        email='answeror+torabot@gmail.com',
        password_hash='whatever',
    )
    assert_is_not_none(user_id)
    return user_id


def test_add_user():
    with g.connection.begin_nested() as trans:
        user_id = prepare_user(g.connection)
        user = get_user_detail_bi_id(g.connection, user_id)
        assert_equal(len(user.emails), 1)
        assert_equal(user.emails[0].label, 'main')
        trans.rollback()


def test_add_email():
    with g.connection.begin_nested() as trans:
        user_id = prepare_user(g.connection)
        add_email_bi_user_id(
            g.connection,
            id=user_id,
            email='answeror+foo@gmail.com',
            label=''
        )
        assert_equal(len(get_emails_bi_user_id(g.connection, user_id)), 2)
        trans.rollback()


def test_del_email():
    with g.connection.begin_nested() as trans:
        user_id = prepare_user(g.connection)
        email_id = add_email_bi_user_id(
            g.connection,
            id=user_id,
            email='answeror+foo@gmail.com',
            label=''
        )
        del_email_bi_id(g.connection, email_id)
        assert_equal(len(get_emails_bi_user_id(g.connection, user_id)), 1)
        trans.rollback()


def test_del_main_email_fail():
    with g.connection.begin_nested() as trans:
        user_id = prepare_user(g.connection)
        emails = get_emails_bi_user_id(g.connection, user_id)
        assert_raises(DeleteMainEmainError, del_email_bi_id, g.connection, emails[0].id)
        trans.rollback()


def test_update_main_email_id():
    with g.connection.begin_nested() as trans:
        user_id = prepare_user(g.connection)
        emails = get_emails_bi_user_id(g.connection, user_id)
        email, label = 'answeror+update@gmail.com', 'update'
        update_email_bi_id(
            g.connection,
            id=emails[0].id,
            email=email,
            label=label
        )
        user = get_user_detail_bi_id(g.connection, user_id)
        assert_equal(user.email, email)
        assert_equal(user.emails[0].text, email)
        assert_equal(user.emails[0].label, label)
        trans.rollback()


def test_update_non_main_email_id():
    with g.connection.begin_nested() as trans:
        user_id = prepare_user(g.connection)
        email_id = add_email_bi_user_id(
            g.connection,
            id=user_id,
            email='answeror+foo@gmail.com',
            label=''
        )
        email, label = 'answeror+update@gmail.com', 'update'
        update_email_bi_id(
            g.connection,
            id=email_id,
            email=email,
            label=label
        )
        user = get_user_detail_bi_id(g.connection, user_id)
        assert_equal(user.emails[-1].text, email)
        assert_equal(user.emails[-1].label, label)
        trans.rollback()


def test_activate_user():
    with g.connection.begin_nested() as trans:
        user_id = prepare_user(g.connection)
        activate_user_bi_id(g.connection, user_id)
        assert user_activated_bi_id(g.connection, user_id)
        emails = get_emails_bi_user_id(g.connection, user_id)
        assert emails[0].activated
        trans.rollback()


def test_inactivate_user():
    with g.connection.begin_nested() as trans:
        user_id = prepare_user(g.connection)
        activate_user_bi_id(g.connection, user_id)
        inactivate_user_bi_id(g.connection, user_id)
        assert not user_activated_bi_id(g.connection, user_id)
        emails = get_emails_bi_user_id(g.connection, user_id)
        assert not emails[0].activated
        trans.rollback()


def test_activate_main_email():
    with g.connection.begin_nested() as trans:
        user_id = prepare_user(g.connection)
        emails = get_emails_bi_user_id(g.connection, user_id)
        activate_email_bi_id(g.connection, emails[0].id)
        assert email_activated_bi_id(g.connection, emails[0].id)
        assert user_activated_bi_id(g.connection, user_id)
        trans.rollback()


def test_inactivate_main_email():
    with g.connection.begin_nested() as trans:
        user_id = prepare_user(g.connection)
        emails = get_emails_bi_user_id(g.connection, user_id)
        activate_email_bi_id(g.connection, emails[0].id)
        inactivate_email_bi_id(g.connection, emails[0].id)
        assert not email_activated_bi_id(g.connection, emails[0].id)
        assert not user_activated_bi_id(g.connection, user_id)
        trans.rollback()


def test_activate_non_main_email():
    with g.connection.begin_nested() as trans:
        user_id = prepare_user(g.connection)
        email_id = add_email_bi_user_id(
            g.connection,
            id=user_id,
            email='answeror+foo@gmail.com',
            label=''
        )
        activate_email_bi_id(g.connection, email_id)
        assert email_activated_bi_id(g.connection, email_id)
        trans.rollback()


def test_inactivate_non_main_email():
    with g.connection.begin_nested() as trans:
        user_id = prepare_user(g.connection)
        email_id = add_email_bi_user_id(
            g.connection,
            id=user_id,
            email='answeror+foo@gmail.com',
            label=''
        )
        activate_email_bi_id(g.connection, email_id)
        inactivate_email_bi_id(g.connection, email_id)
        assert not email_activated_bi_id(g.connection, email_id)
        trans.rollback()


def test_email_count_limit():
    with g.connection.begin_nested() as trans:
        user_id = prepare_user(g.connection)
        for i in range(2):
            add_email_bi_user_id(
                g.connection,
                id=user_id,
                email='answeror+%d@gmail.com' % i,
                label=''
            )
        assert_raises(
            EmailCountLimitError,
            add_email_bi_user_id,
            g.connection,
            id=user_id,
            email='answeror+fail@gmail.com',
            label=''
        )
        trans.rollback()


def test_set_password_hash_bi_email():
    with g.connection.begin_nested() as trans:
        prepare_user(g.connection)
        email = 'answeror+torabot@gmail.com'
        op.set_password_hash_bi_email(g.connection, email, 'new hash')
        assert_equal(
            op.get_password_hash_bi_email(g.connection, email),
            'new hash'
        )
        trans.rollback()


def test_get_user_id_bi_email():
    with g.connection.begin_nested() as trans:
        user_id = prepare_user(g.connection)
        assert_equal(
            op.get_user_id_bi_email(g.connection, 'answeror+torabot@gmail.com'),
            user_id
        )
        assert_is_none(
            op.get_user_id_bi_email(g.connection, 'noanswer@gmail.com')
        )
        trans.rollback()


def test_has_email():
    with g.connection.begin_nested() as trans:
        prepare_user(g.connection)
        assert op.has_email(g.connection, 'answeror+torabot@gmail.com')
        assert not op.has_email(g.connection, 'noanswer@gmail.com')
        trans.rollback()
