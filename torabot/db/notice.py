from ..ut.bunch import Bunch


def get_notices_bi_user_id(conn, user_id):
    result = conn.execute('''
        select
            n0.id,
            n0.user_id,
            n0.ctime,
            n0.status,
            change.old_status,
            change.new_status,
            art.title,
            art.uri
        from (
            select * from notice
            where user_id = %s
        ) as n0
        inner join change on n0.change_id = change.id
        inner join art on change.art_id = art.id
        order by n0.ctime desc
    ''', (user_id,))
    return [Bunch(**row) for row in result.fetchall()]


def get_pending_notices_bi_user_id(conn, user_id):
    result = conn.execute('''
        select
            n0.id,
            n0.user_id,
            n0.ctime,
            n0.status,
            change.old_status,
            change.new_status,
            art.title,
            art.uri
        from (
            select * from notice
            where user_id = %s and status = %s
        ) as n0
        inner join change on n0.change_id = change.id
        inner join art on change.art_id = art.id
        order by n0.ctime desc
    ''', (user_id, 'pending'))
    return [Bunch(**row) for row in result.fetchall()]
