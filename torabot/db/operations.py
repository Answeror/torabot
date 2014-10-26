from nose.tools import assert_in
from functools import wraps
import sqlalchemy.exc
from sqlalchemy.sql import text as sql
from psycopg2.extras import Json
from datetime import datetime
import jsonpickle
import json
from fn.iters import chain
import hashlib
from email.utils import parseaddr
from ..ut.bunch import bunchr
from .ut import ignore_none


NOTICE_PAGE_SIZE = 2147483647


def guard(f):
    @wraps(f)
    def inner(conn, *args, **kargs):
        from . import db

        try:
            return f(conn, *args, **kargs)
        except sqlalchemy.exc.DataError as e:
            raise db.InvalidArgumentError from e
        except sqlalchemy.exc.IntegrityError as e:
            if 'duplicate' in str(e):
                raise db.UniqueConstraintError(str(e)) from e
            if 'update or delete on table "email" violates foreign key constraint "watch_email_id_fkey" on table "watch"' in str(e):
                raise db.DeleteEmailInUseError from e
            raise
        except sqlalchemy.exc.InternalError as e:
            if 'cannot delete main email of' in str(e):
                raise db.DeleteMainEmainError from e
            if 'email count reach limit' in str(e):
                raise db.EmailCountLimitError from e
            if 'watch count reach limit' in str(e):
                raise db.WatchCountLimitError from e
            raise
    return inner


def fill_id(conn, user_id, email_id):
    from . import db

    assert user_id is not None or email_id is not None

    if email_id is None:
        email_id = conn.execute(
            sql('select id from email where user_id = :user_id order by ctime limit 1'),
            user_id=user_id
        ).fetchone()
        if email_id:
            email_id = email_id[0]

    if user_id is None:
        user_id = conn.execute(
            sql('select user_id from email where id = :email_id'),
            email_id=email_id
        ).fetchone()
        if user_id:
            user_id = user_id[0]

    if user_id is None:
        raise db.UserNotExistError()
    if email_id is None:
        raise db.EmailNotExistError()

    return user_id, email_id


@guard
def watch(conn, query_id, user_id=None, email_id=None, name=None):
    user_id, email_id = fill_id(conn, user_id, email_id)
    if user_id is None or email_id is None:
        return

    conn.execute(sql(
        '''
        insert into watch (user_id, query_id, email_id%s)
        select :user_id, :query_id, :email_id%s
        where not exists (
            select 1 from watch
            where email_id = :email_id and query_id = :query_id
        )
        ''' % (('', '') if name is None else (', name', ', :name'))
    ), user_id=user_id, query_id=query_id, email_id=email_id, name=name)


def unwatch(conn, query_id, user_id=None, email_id=None):
    user_id, email_id = fill_id(conn, user_id, email_id)
    if user_id is None or email_id is None:
        return

    conn.execute(sql(
        '''
        delete from watch
        where email_id = :email_id and query_id = :query_id
        '''
    ), email_id=email_id, query_id=query_id)


def watching(conn, query_id, user_id=None, email_id=None):
    user_id, email_id = fill_id(conn, user_id, email_id)
    if user_id is None or email_id is None:
        return

    return conn.execute((
        'select 1 from watch '
        'where user_id = %s and query_id = %s'
    ), (user_id, query_id)).fetchone() is not None


def get_watch_count_bi_user_id(conn, user_id):
    return conn.execute(
        sql('select count(1) from watch where user_id = :user_id'),
        user_id=user_id
    ).fetchone()[0]


def get_watches_bi_user_id(conn, user_id, offset=None, limit=None):
    result = conn.execute(sql('\n'.join([
        '''
        select
            w0.user_id,
            w0.query_id,
            w0.name,
            w0.ctime,
            q0.kind query_kind,
            q0.text query_text,
            q0.mtime query_mtime,
            w0.email_id,
            e0.text email_text,
            e0.label email_label,
            e0.activated email_activated
        from watch w0
            inner join query q0 on w0.query_id = q0.id
            inner join email e0 on w0.email_id = e0.id
        where w0.user_id = :user_id
        order by w0.ctime desc
        ''',
        '' if offset is None else 'offset :offset',
        '' if limit is None else 'limit :limit'
    ])), user_id=user_id, offset=offset, limit=limit)
    return [bunchr(**row) for row in result.fetchall()]


def rename_watch(conn, query_id, name, user_id=None, email_id=None):
    user_id, email_id = fill_id(conn, user_id, email_id)
    if user_id is None or email_id is None:
        return

    conn.execute(sql(
        '''
        update watch set name = :name
        where email_id = :email_id and query_id = :query_id
        '''
    ), email_id=email_id, query_id=query_id, name=name)


def get_email_watch_states(conn, user_id, query_id):
    return [bunchr(**row) for row in conn.execute(sql(
        '''
        select e0.*, (select count(1) from watch as w0 where w0.email_id = e0.id and w0.query_id = :query_id) watching
        from email e0
        where e0.user_id = :user_id
        order by e0.ctime
        '''
    ), user_id=user_id, query_id=query_id).fetchall()]


@guard
def add_user(conn, name, email, password_hash):
    return conn.execute(sql(
        '''
        insert into "user" (name, email, password_hash)
        values (:name, :email, :password_hash)
        returning *
        '''
    ), name=name, email=email, password_hash=password_hash).fetchone()[0]


@guard
def get_user_id_bi_openid(conn, openid):
    ret = conn.execute('select id from "user" where openid = %s', (openid,)).fetchone()
    return None if ret is None else ret[0]


@guard
def get_user_name_bi_openid(conn, openid):
    ret = conn.execute('select name from "user" where openid = %s', (openid,)).fetchone()
    return None if ret is None else ret[0]


@guard
def get_user_name_bi_id(conn, id):
    ret = conn.execute(sql('select name from "user" where id = :id'), id=id).fetchone()
    return None if ret is None else ret[0]


@guard
def get_user_email_bi_id(conn, id):
    ret = conn.execute('select email from "user" where id = %s', (id,)).fetchone()
    return None if ret is None else ret[0]


@guard
def get_user_bi_id(conn, id):
    ret = conn.execute('select * from "user" where id = %s', (id,)).fetchone()
    return None if ret is None else bunchr(**ret)


@guard
def set_email(conn, id, email):
    conn.execute(
        'update "user" set email = %s where id = %s',
        (email, id)
    )


@guard
def get_users(conn, offset=None, limit=None):
    result = conn.execute(sql('\n'.join([
        'select * from "user" order by id',
        '' if offset is None else 'offset :offset',
        '' if limit is None else 'limit :limit'
    ])), **dict(offset=offset, limit=limit))
    return [bunchr(**row) for row in result.fetchall()]


def check_user_order_field(name):
    assert_in(name, [
        'id',
        'name',
        'email',
        'ctime',
    ])


@guard
def get_users_detail(conn, offset=None, limit=None, order_by=None, desc=False):
    ignore_none(check_user_order_field)(order_by)
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


@guard
def get_user_detail_bi_id(conn, id):
    return enrich(conn, conn.execute(sql(
        '''
        select u0.*, (select count(1) from watch as w0 where w0.user_id = u0.id) watch_count
        from "user" as u0
        where u0.id = :id
        '''
    ), id=id).fetchone())


@guard
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


@guard
def get_user_detail_bi_email_id(conn, id):
    return enrich(conn, conn.execute(sql(
        '''
        select u0.*, (select count(1) from watch as w0 where w0.user_id = u0.id) watch_count
        from "user" as u0 inner join email e0 on u0.id = e0.user_id
        where e0.id = :id
        '''
    ), id=id).fetchone())


@guard
def get_emails_bi_user_id(conn, id):
    return [bunchr(**row) for row in conn.execute(
        sql('select * from email where user_id = :id order by ctime'),
        id=id
    ).fetchall()]


@guard
def get_email_bi_id(conn, id):
    ret = conn.execute(
        sql('select * from email where id = :id'),
        id=id
    ).fetchone()
    return None if ret is None else bunchr(**ret)


@guard
def add_email_bi_user_id(conn, id, email, label):
    from . import db

    # http://stackoverflow.com/a/14485817/238472
    if not email or parseaddr(email) == ('', ''):
        raise db.InvalidEmailError(email)
    return conn.execute(sql(
        '''
        insert into email (text, label, user_id)
        values (:text, :label, :user_id)
        returning *
        '''
    ), text=email, label=label, user_id=id).fetchone()[0]


@guard
def del_email_bi_id(conn, id):
    conn.execute(
        sql('delete from email where id = :id'),
        id=id
    )


@guard
def get_user_count(conn):
    return conn.execute('select count(1) from "user"').fetchone()[0]


@guard
def set_user_field_bi_id(conn, id, field, value):
    assert_in(field, ('name', 'email', 'openid', 'maxwatch'))
    conn.execute(
        sql('update "user" set %s = :value where id = :id' % field),
        id=id,
        value=value
    )


@guard
def has_user_bi_openid(conn, openid):
    return conn.execute(
        sql('select 1 from "user" where openid = :openid'),
        openid=openid
    ).fetchone() is not None


@guard
def has_user_bi_id(conn, id):
    return conn.execute(
        sql('select 1 from "user" where id = :id'),
        id=id
    ).fetchone() is not None


@guard
def activate_user_bi_id(conn, id):
    conn.execute(sql('update "user" set activated = TRUE where id = :id'), id=id)


@guard
def activate_email_bi_id(conn, id):
    conn.execute(sql('update email set activated = TRUE where id = :id'), id=id)


@guard
def inactivate_user_bi_id(conn, id):
    conn.execute(sql('update "user" set activated = FALSE where id = :id'), id=id)


@guard
def inactivate_email_bi_id(conn, id):
    conn.execute(sql('update email set activated = FALSE where id = :id'), id=id)


@guard
def user_activated_bi_id(conn, id):
    return conn.execute(
        sql('select activated from "user" where id = :id'),
        id=id
    ).fetchone()[0]


@guard
def email_activated_bi_id(conn, id):
    return conn.execute(
        sql('select activated from email where id = :id'),
        id=id
    ).fetchone()[0]


@guard
def update_email_bi_id(conn, id, email, label):
    conn.execute(
        sql('update email set text = :text, label = :label where id = :id'),
        id=id,
        text=email,
        label=label
    )


def has_change(conn):
    return conn.execute('select * from change').fetchone() is not None


def add_one_query_changes(conn, query_id, data):
    data = list(data)
    if not data:
        return []
    result = conn.execute(''.join([
        'insert into change (query_id, data, hash) values ',
        ', '.join('(%s, %s, %s)' for i in range(len(data))),
        ' returning *',
    ]), list(chain(*[(query_id, Json(d), _encode_dict(d)) for d in data])))
    return [row[0] for row in result.fetchall()]


def del_old_changes(conn, before, limit):
    conn.execute(sql(
        '''
        delete from change
        where change.id in (
            select c0.id
            from change as c0
            where c0.ctime < :before
            limit :limit
        )
        '''
    ), before=before, limit=limit)


def get_change_count(conn):
    return conn.execute(sql('select count(1) from change')).fetchone()[0]


def _encode_dict(d):
    return hashlib.md5(
        json.dumps(d, sort_keys=True).encode('ascii')
    ).hexdigest()


def add_one_query_changes_unique(conn, query_id, data, past):
    data = list(data)
    if not data:
        return []

    params = {}
    for i, d in enumerate(d for d in data):
        params['d%d' % i] = Json(d)
        params['h%d' % i] = _encode_dict(d)

    result = conn.execute(
        sql(''.join([
            '''
            insert into change (query_id, data, hash)
            select :query_id, c0.data, c0.hash from ( values
            ''',
            ', '.join('(:d{0} ::json, :h{0})'.format(i) for i in range(len(data))),
            ') as c0(data, hash) ',
            '''
            where not exists (
                select 1 from change
                where
                    query_id = :query_id and
                    ctime >= :begin and
                    hash = c0.hash
            )
            returning *
            '''
        ])),
        query_id=query_id,
        begin=datetime.now() - past,
        **params
    )
    return [row[0] for row in result.fetchall()]


def get_notices_bi_user_id(conn, user_id, page=0, room=NOTICE_PAGE_SIZE):
    result = conn.execute(sql(
        '''
        select
            n0.id,
            n0.user_id,
            n0.ctime,
            n0.status,
            q0.kind kind,
            c0.data change,
            n0.email
        from (
            select * from notice
            where user_id = :user_id
        ) n0
        inner join change c0 on n0.change_id = c0.id
        inner join query q0 on c0.query_id = q0.id
        order by n0.ctime desc
        offset :offset
        limit :limit
        '''
    ), user_id=user_id, offset=page * room, limit=room)
    return [make(**row) for row in result.fetchall()]


def make(change, **kargs):
    return bunchr(change=jsonpickle.decode(json.dumps(change)), **kargs)


def get_notice_count_bi_user_id(conn, user_id):
    return conn.execute(sql('''
        select count(*) from notice
        where user_id = :user_id
    '''), user_id=user_id).fetchone()[0]


def get_pending_notices_bi_user_id(conn, user_id, page=0, room=NOTICE_PAGE_SIZE):
    result = conn.execute(sql(
        '''
        select
            n0.id,
            n0.user_id,
            n0.ctime,
            n0.status,
            q0.kind kind,
            c0.data change,
            n0.email
        from (
            select * from notice
            where user_id = :user_id and status = :status
        ) n0
        inner join change c0 on n0.change_id = c0.id
        inner join query q0 on c0.query_id = q0.id
        order by n0.ctime desc
        offset :offset
        limit :limit
    '''), user_id=user_id, status='pending', offset=page * room, limit=room)
    return [make(**row) for row in result.fetchall()]


def get_pending_notice_count_bi_user_id(conn, user_id):
    return conn.execute(sql('''
        select count(*) from notice
        where user_id = :user_id and status = :status
    '''), user_id=user_id, status='pending').fetchone()[0]


def get_pending_notices(conn):
    result = conn.execute(sql(
        '''
        select
            n0.id,
            n0.user_id,
            n0.ctime,
            n0.status,
            q0.kind kind,
            c0.data change,
            n0.email
        from (
            select * from notice
            where status = :status
        ) n0
        inner join change c0 on n0.change_id = c0.id
        inner join query q0 on c0.query_id = q0.id
        order by n0.ctime desc
        '''
    ), status='pending')
    return [make(**row) for row in result.fetchall()]


def mark_notice_sent(conn, id):
    conn.execute(
        sql('update notice set status = :status where id = :id'),
        status='sent',
        id=id
    )


def count_recent_notice_bi_user_id(conn, user_id, interval):
    return conn.execute(sql(
        '''
        select count(1) from notice
        where user_id = :user_id and ctime >= :begin
        '''
    ), user_id=user_id, begin=datetime.utcnow() - interval).fetchone()[0]


def add_query(conn, kind, text, result={}):
    ret = conn.execute(sql('''
        insert into query (kind, text, result)
        values (:kind, :text, :result)
        returning *
    '''), kind=kind, text=text, result=Json(result)).fetchone()
    return ret[0]


def get_or_add_query_bi_kind_and_text(conn, kind, text):
    result = conn.execute(
        sql('select * from get_or_add_query_bi_kind_and_text(:kind, :text)'),
        kind=kind, text=text
    )
    return mq(**result.fetchone())


def set_query_result(conn, query_id, result):
    conn.execute(
        sql('update query set result = :result where id = :id'),
        id=query_id,
        result=Json(result)
    )


def get_query_bi_kind_and_text(conn, kind, text):
    ret = conn.execute(
        sql('select * from query where kind = :kind and text = :text'),
        kind=kind,
        text=text
    ).fetchone()
    return None if ret is None else mq(**ret)


def get_query_count(conn):
    return conn.execute(sql('select count(*) from query')).fetchone()[0]


def has_query_bi_kind_and_text(conn, kind, text):
    return conn.execute(
        sql('select 1 from query where kind = :kind and text = :text'),
        kind=kind,
        text=text
    ).fetchone() is not None


def get_need_sync_queries(conn, offset=None, limit=None):
    result = conn.execute(sql('\n'.join([
        '''
        select * from query as q0
        where exists (
            select 1 from watch as w0
            where w0.query_id = q0.id and q0.next_sync_time is null
        ) or q0.next_sync_time <= (now() at time zone 'utc')
        order by q0.id
        ''',
        '' if offset is None else 'offset :offset',
        '' if limit is None else 'limit :limit'
    ])), **dict(offset=offset, limit=limit))
    return [mq(**row) for row in result.fetchall()]


def set_next_sync_time(conn, id, time):
    conn.execute(sql(
        '''
        update query set next_sync_time = :time
        where id = :id
        '''
    ), id=id, time=time)


def set_next_sync_time_bi_kind_and_text(conn, kind, text, time):
    conn.execute(sql(
        '''
        update query set next_sync_time = :time
        where kind = :kind and text = :text
        '''
    ), kind=kind, text=text, time=time)


def get_active_queries(conn, offset=None, limit=None, order_by=None, desc=False):
    ignore_none(check_query_order_field)(order_by)
    result = conn.execute(sql('\n'.join([
        '''
        select * from query as q0
        where exists (
            select 1 from watch as w0
            where w0.query_id = q0.id
        )
        ''',
        '' if order_by is None else 'order by q0.%s' % order_by,
        '' if order_by is None or not desc else 'desc',
        '' if offset is None else 'offset :offset',
        '' if limit is None else 'limit :limit'
    ])), **dict(offset=offset, limit=limit))
    return [mq(**row) for row in result.fetchall()]


def get_sorted_active_queries(conn, offset=None, limit=None):
    result = conn.execute(sql('\n'.join([
        '''
        select * from query as q0
        where exists (
            select 1 from watch as w0
            where w0.query_id = q0.id
        )
        order by q0.ctime
        ''',
        '' if offset is None else 'offset :offset',
        '' if limit is None else 'limit :limit'
    ])), **dict(offset=offset, limit=limit))
    return [mq(**row) for row in result.fetchall()]


def get_active_query_count(conn):
    return conn.execute(sql(
        '''
        select count(1) from query as q0
        where exists (
            select 1 from watch as w0
            where w0.query_id = q0.id
        )
        '''
    )).fetchone()[0]


def touch_query_bi_id(conn, id):
    conn.execute(
        sql('update query set mtime = :mtime where id = :id'),
        id=id,
        mtime=datetime.utcnow()
    )


def get_query_mtime_bi_kind_and_text(conn, kind, text):
    ret = conn.execute(
        sql('select mtime from query where kind = :kind and text = :text'),
        kind=kind,
        text=text
    ).fetchone()
    return None if ret is None else ret[0]


def check_query_order_field(name):
    assert_in(name, [
        'id',
        'ctime',
    ])


def get_queries(conn, offset=None, limit=None, order_by=None, desc=False):
    ignore_none(check_query_order_field)(order_by)
    result = conn.execute(sql('\n'.join([
        '''
        select * from query as q0
        ''',
        '' if order_by is None else 'order by q0.%s' % order_by,
        '' if order_by is None or not desc else 'desc',
        '' if offset is None else 'offset :offset',
        '' if limit is None else 'limit :limit'
    ])), **dict(offset=offset, limit=limit))
    return [mq(**row) for row in result.fetchall()]


def mq(result, **kargs):
    return bunchr(result=jsonpickle.decode(json.dumps(result)), **kargs)


def get_query_bi_id(conn, id):
    ret = conn.execute(
        sql('select * from query where id = :id'),
        id=id
    ).fetchone()
    return None if ret is None else mq(**ret)


def is_query_active_bi_id(conn, id):
    return conn.execute(sql(
        '''
        select 1 from watch as w0
        where w0.query_id = :id
        '''
    ), id=id).fetchone() is not None


@guard
def set_query_field_bi_id(conn, id, field, value):
    conn.execute(
        sql('update query set %s = :value where id = :id' % field),
        id=id,
        value=value
    )


def del_query_bi_id(conn, id):
    conn.execute(
        sql('delete from query where id = :id'),
        id=id
    )


def del_inactive_queries(conn, before, limit):
    conn.execute(sql(
        '''
        delete from query
        where query.id in (
            select q0.id
            from query as q0
            where q0.ctime < :before and not exists (
                select 1 from watch as w0
                where w0.query_id = q0.id
            )
            limit :limit
        )
        '''
    ), id=id, before=before, limit=limit)


def set_password_hash_bi_email(conn, email, password_hash):
    conn.execute(
        sql(
            '''
            update "user" set password_hash = :password_hash
            where id = (
                select user_id from email
                where text = :email
            )
            '''
        ),
        email=email,
        password_hash=password_hash
    )


def get_password_hash_bi_email(conn, email):
    ret = conn.execute(
        sql(
            '''
            select password_hash from "user"
            where id = (
                select user_id from email
                where text = :email
            )
            '''
        ),
        email=email
    ).fetchone()
    return None if ret is None else ret[0]


def get_user_id_bi_email(conn, email):
    ret = conn.execute(
        sql('select user_id from email where text = :email'),
        email=email
    ).fetchone()
    return None if ret is None else ret[0]


def has_email(conn, email):
    return conn.execute(
        sql('select 1 from email where text = :email'),
        email=email
    ).fetchone() is not None
