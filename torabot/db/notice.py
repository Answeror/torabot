from sqlalchemy.sql import text as sql
from ..ut.bunch import Bunch


def get_notices_bi_user_id(conn, user_id):
    result = conn.execute(sql('''
        select
            n0.id,
            n0.user_id,
            n0.ctime,
            n0.status,
            c0.data as change
        from (
            select * from notice
            where user_id = :user_id
        ) as n0
        inner join change as c0 on n0.change_id = c0.id
        order by n0.ctime desc
    '''), user_id=user_id)
    return [Bunch(**row) for row in result.fetchall()]


def get_pending_notices_bi_user_id(conn, user_id):
    result = conn.execute(sql('''
        select
            n0.id,
            n0.user_id,
            n0.ctime,
            n0.status,
            c0.data as change
        from (
            select * from notice
            where user_id = :user_id and status = :status
        ) as n0
        inner join change as c0 on n0.change_id = c0.id
        order by n0.ctime desc
    '''), user_id=user_id, status='pending')
    return [Bunch(**row) for row in result.fetchall()]


def get_pending_notices(conn):
    result = conn.execute(sql('''
        select
            n0.id,
            n0.user_id,
            n0.ctime,
            n0.status,
            c0.data as change
        from (
            select * from notice
            where status = :status
        ) as n0
        inner join change as c0 on n0.change_id = c0.id
        order by n0.ctime desc
    '''), status='pending')
    return [Bunch(**row) for row in result.fetchall()]


def mark_notice_sent(conn, id):
    conn.execute(
        sql('update notice set status = :status where id = :id'),
        status='sent',
        id=id
    )
