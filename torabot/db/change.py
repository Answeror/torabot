from fn.iters import chain
from psycopg2.extras import Json
from sqlalchemy.sql import text as sql


def has_change(conn):
    return conn.execute('select * from change').fetchone() is not None


def add_one_query_changes(conn, query_id, data):
    data = list(data)
    if not data:
        return []
    result = conn.execute(''.join([
        'insert into change (query_id, data) values ',
        ', '.join('(%s, %s)' for i in range(len(data))),
        ' returning *',
    ]), list(chain(*[(query_id, Json(d)) for d in data])))
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
