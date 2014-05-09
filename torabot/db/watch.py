from sqlalchemy.sql import text as sql
from ..ut.bunch import bunchr


def fill_id(conn, user_id, email_id):
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

    return user_id, email_id


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


def get_watches_bi_user_id(conn, user_id):
    result = conn.execute(sql(
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
        '''
    ), user_id=user_id)
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
