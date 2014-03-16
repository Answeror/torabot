from fn.iters import chain, starmap
from ..ut.bunch import Bunch


def add_query(conn, text):
    ret = conn.execute((
        'insert into query (text) '
        'values (%s) '
        'returning *'
    ), (text,)).fetchone()
    return ret[0]


def add_result(conn, query_id, art_id, rank):
    ret = conn.execute((
        'insert into result (query_id, art_id, rank) '
        'values (%s, %s, %s) '
        'returning *'
    ), (query_id, art_id, rank)).fetchone()
    return ret[0]


def add_results(conn, query_id, ranks):
    ranks = list(ranks)
    if ranks:
        result = conn.execute(''.join([
            'insert into result (query_id, art_id, rank) values ',
            ', '.join('(%s, %s, %s)' for i in range(len(ranks))),
            ' returning *',
        ]), list(chain(*[(query_id, art_id, rank) for art_id, rank in ranks])))
        return [row[0] for row in result.fetchall()]
    else:
        return []


def del_results(conn, query_id):
    conn.execute('delete from result where query_id = %s', (query_id,))


def set_results(conn, query_id, art_ids):
    del_results(conn, query_id)
    add_results(conn, query_id, starmap(lambda a, b: (b, a), enumerate(art_ids)))


def result_count_bi_query_id(conn, query_id):
    return conn.execute((
        'select count(*) from result '
        'where query_id = %s'
    ), (query_id,)).fetchone()[0]


def put_query(conn, text):
    conn.execute((
        'insert into query (text) '
        'select %(text)s '
        'where not exists (select 1 from query '
        'where text = %(text)s)'
    ), dict(text=text))


def get_query_bi_text(conn, text):
    ret = conn.execute('select * from query where text = %s', (text,)).fetchone()
    return None if ret is None else Bunch(**ret)


def get_arts_bi_query_id(conn, query_id, offset=None, limit=None):
    parts = [
        'select * from art inner join result on art.id = result.art_id ',
        'where result.query_id = %(query_id)s ',
        'order by rank ',
    ]
    params = dict(query_id=query_id)

    if offset is not None:
        parts.append('offset %(offset)s ')
        params['offset'] = offset

    if limit is not None:
        parts.append('limit %(limit)s ')
        params['limit'] = limit

    result = conn.execute(''.join(parts), params)
    return [Bunch(**row) for row in result.fetchall()]


def set_total(conn, id, total):
    conn.execute((
        'update query set total = %s '
        'where id = %s'
    ), (total, id))


def query_count(conn):
    return conn.execute('select count(*) from query').fetchone()[0]


def has_query_bi_text(conn, text):
    return conn.execute(
        'select 1 from query where text = %s',
        (text,)
    ).fetchone() is not None


def get_sorted_queries(conn):
    result = conn.execute('select * from query order by ctime')
    return [Bunch(**row) for row in result.fetchall()]
