from fn.iters import chain
from psycopg2.extras import Json
from sqlalchemy.sql import text as sql
from datetime import datetime
import hashlib
import json


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
