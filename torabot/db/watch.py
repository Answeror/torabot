from sqlalchemy.sql import text as sql
from ..ut.bunch import bunchr


def watch(conn, user_id, query_id):
    conn.execute((
        'insert into watch (user_id, query_id) '
        'select %(user_id)s, %(query_id)s '
        'where not exists (select 1 from watch '
        'where user_id = %(user_id)s and query_id = %(query_id)s)'
    ), dict(user_id=user_id, query_id=query_id))


def unwatch(conn, user_id, query_id):
    conn.execute((
        'delete from watch '
        'where user_id = %s and query_id = %s'
    ), (user_id, query_id))


def watching(conn, user_id, query_id):
    return conn.execute((
        'select 1 from watch '
        'where user_id = %s and query_id = %s'
    ), (user_id, query_id)).fetchone() is not None


def get_watches_bi_user_id(conn, user_id):
    result = conn.execute(sql(
        '''
        select
            user_id,
            query_id,
            watch.name,
            watch.ctime,
            query.kind as query_kind,
            query.text as query_text,
            query.mtime as query_mtime
        from watch inner join query on watch.query_id = query.id
        where user_id = :user_id
        order by watch.ctime desc
        '''
    ), user_id=user_id)
    return [bunchr(**row) for row in result.fetchall()]


def rename_watch(conn, user_id, query_id, name):
    conn.execute(sql(
        '''
        update watch set name = :name
        where user_id = :user_id and query_id = :query_id
        '''
    ), user_id=user_id, query_id=query_id, name=name)
