from nose.tools import assert_in
from sqlalchemy.sql import text as sql
from email.utils import parseaddr
from ..ut.bunch import bunchr
from .error import error_guard, InvalidEmailError
from .ut import ignore_none


@error_guard
def add_user(conn, name, email, openid):
    return conn.execute((
        'insert into "user" (name, email, openid)'
        'values (%s, %s, %s) '
        'returning *'
    ), (name, email, openid)).fetchone()[0]


@error_guard
def get_user_id_bi_openid(conn, openid):
    ret = conn.execute('select id from "user" where openid = %s', (openid,)).fetchone()
    return None if ret is None else ret[0]


@error_guard
def get_user_name_bi_openid(conn, openid):
    ret = conn.execute('select name from "user" where openid = %s', (openid,)).fetchone()
    return None if ret is None else ret[0]


@error_guard
def get_user_name_bi_id(conn, id):
    ret = conn.execute(sql('select name from "user" where id = :id'), id=id).fetchone()
    return None if ret is None else ret[0]


@error_guard
def get_user_email_bi_id(conn, id):
    ret = conn.execute('select email from "user" where id = %s', (id,)).fetchone()
    return None if ret is None else ret[0]


@error_guard
def get_user_bi_id(conn, id):
    ret = conn.execute('select * from "user" where id = %s', (id,)).fetchone()
    return None if ret is None else bunchr(**ret)


@error_guard
def set_email(conn, id, email):
    conn.execute(
        'update "user" set email = %s where id = %s',
        (email, id)
    )


@error_guard
def get_users(conn, offset=None, limit=None):
    result = conn.execute(sql('\n'.join([
        'select * from "user" order by id',
        '' if offset is None else 'offset :offset',
        '' if limit is None else 'limit :limit'
    ])), **dict(offset=offset, limit=limit))
    return [bunchr(**row) for row in result.fetchall()]


def check_order_field(name):
    assert_in(name, [
        'id',
        'name',
        'email',
        'ctime',
    ])


@error_guard
def get_users_detail(conn, offset=None, limit=None, order_by=None, desc=False):
    ignore_none(check_order_field)(order_by)
    result = conn.execute(sql('\n'.join([
        '''
        select u0.*, (select count(1) from watch as w0 where w0.user_id = u0.id) watch_count
        from "user" as u0
        ''',
        '' if order_by is None else 'order by u0.%s' % order_by,
        '' if order_by is None or not desc else 'desc',
        '' if offset is None else 'offset :offset',
        '' if limit is None else 'limit :limit'
    ])), **dict(offset=offset, limit=limit))
    return [bunchr(**row) for row in result.fetchall()]


@error_guard
def get_user_detail_bi_id(conn, id):
    return enrich(conn, conn.execute(sql(
        '''
        select u0.*, (select count(1) from watch as w0 where w0.user_id = u0.id) watch_count
        from "user" as u0
        where u0.id = :id
        '''
    ), id=id).fetchone())


@error_guard
def get_user_detail_bi_openid(conn, openid):
    return enrich(conn, conn.execute(sql(
        '''
        select u0.*, (select count(1) from watch as w0 where w0.user_id = u0.id) watch_count
        from "user" as u0
        where u0.openid = :openid
        '''
    ), openid=openid).fetchone())


def enrich(conn, ret):
    if ret is None:
        return None
    user = bunchr(**ret)
    user.emails = get_emails_bi_user_id(conn, user.id)
    return user


@error_guard
def get_user_detail_bi_email_id(conn, id):
    return enrich(conn, conn.execute(sql(
        '''
        select u0.*, (select count(1) from watch as w0 where w0.user_id = u0.id) watch_count
        from "user" as u0 inner join email e0 on u0.id = e0.user_id
        where e0.id = :id
        '''
    ), id=id).fetchone())


@error_guard
def get_emails_bi_user_id(conn, id):
    return [bunchr(**row) for row in conn.execute(
        sql('select * from email where user_id = :id order by ctime'),
        id=id
    ).fetchall()]


@error_guard
def get_email_bi_id(conn, id):
    ret = conn.execute(
        sql('select * from email where id = :id'),
        id=id
    ).fetchone()
    return None if ret is None else bunchr(**ret)


@error_guard
def add_email_bi_user_id(conn, id, email, label):
    # http://stackoverflow.com/a/14485817/238472
    if not email or parseaddr(email) == ('', ''):
        raise InvalidEmailError(email)
    return conn.execute(sql(
        '''
        insert into email (text, label, user_id)
        values (:text, :label, :user_id)
        returning *
        '''
    ), text=email, label=label, user_id=id).fetchone()[0]


@error_guard
def del_email_bi_id(conn, id):
    conn.execute(
        sql('delete from email where id = :id'),
        id=id
    )


@error_guard
def get_user_count(conn):
    return conn.execute('select count(1) from "user"').fetchone()[0]


@error_guard
def set_user_field_bi_id(conn, id, field, value):
    assert_in(field, ('name', 'email', 'openid', 'maxwatch'))
    conn.execute(
        sql('update "user" set %s = :value where id = :id' % field),
        id=id,
        value=value
    )


@error_guard
def has_user_bi_openid(conn, openid):
    return conn.execute(
        sql('select 1 from "user" where openid = :openid'),
        openid=openid
    ).fetchone() is not None


@error_guard
def activate_user_bi_id(conn, id):
    conn.execute(sql('update "user" set activated = TRUE where id = :id'), id=id)


@error_guard
def activate_email_bi_id(conn, id):
    conn.execute(sql('update email set activated = TRUE where id = :id'), id=id)


@error_guard
def inactivate_user_bi_id(conn, id):
    conn.execute(sql('update "user" set activated = FALSE where id = :id'), id=id)


@error_guard
def inactivate_email_bi_id(conn, id):
    conn.execute(sql('update email set activated = FALSE where id = :id'), id=id)


@error_guard
def user_activated_bi_id(conn, id):
    return conn.execute(
        sql('select activated from "user" where id = :id'),
        id=id
    ).fetchone()[0]


@error_guard
def email_activated_bi_id(conn, id):
    return conn.execute(
        sql('select activated from email where id = :id'),
        id=id
    ).fetchone()[0]


@error_guard
def update_email_bi_id(conn, id, email, label):
    conn.execute(
        sql('update email set text = :text, label = :label where id = :id'),
        id=id,
        text=email,
        label=label
    )
