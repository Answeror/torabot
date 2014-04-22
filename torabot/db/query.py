from sqlalchemy.sql import text as sql
from psycopg2.extras import Json
from datetime import datetime
from ..ut.bunch import bunchr
from .error import error_guard


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
    return bunchr(**result.fetchone())


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
    return None if ret is None else bunchr(**ret)


def get_query_count(conn):
    return conn.execute(sql('select count(*) from query')).fetchone()[0]


def has_query_bi_kind_and_text(conn, kind, text):
    return conn.execute(
        sql('select 1 from query where kind = :kind and text = :text'),
        kind=kind,
        text=text
    ).fetchone() is not None


def get_active_queries(conn, offset=None, limit=None):
    result = conn.execute(sql('\n'.join([
        '''
        select * from query as q0
        where exists (
            select 1 from watch as w0
            where w0.query_id = q0.id
        )
        order by q0.id
        ''',
        '' if offset is None else 'offset :offset',
        '' if limit is None else 'limit :limit'
    ])), **dict(offset=offset, limit=limit))
    return [bunchr(**row) for row in result.fetchall()]


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
    return [bunchr(**row) for row in result.fetchall()]


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


def get_queries(conn, offset=None, limit=None):
    result = conn.execute(sql('\n'.join([
        '''
        select * from query as q0
        order by q0.id
        ''',
        '' if offset is None else 'offset :offset',
        '' if limit is None else 'limit :limit'
    ])), **dict(offset=offset, limit=limit))
    return [bunchr(**row) for row in result.fetchall()]


def get_query_bi_id(conn, id):
    ret = conn.execute(
        sql('select * from query where id = :id'),
        id=id
    ).fetchone()
    return None if ret is None else bunchr(**ret)


@error_guard
def set_query_field_bi_id(conn, id, field, value):
    conn.execute(
        sql('update query set %s = :value where id = :id' % field),
        id=id,
        value=value
    )
