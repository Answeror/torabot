from fn.iters import chain, starmap


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
    result = conn.execute(''.join([
        'insert into result (query_id, art_id, rank) values ',
        ', '.join('(%s, %s, %s)' for i in range(len(ranks))),
        ' returning *',
    ]), list(chain(*[(query_id, art_id, rank) for art_id, rank in ranks])))
    return [row[0] for row in result.fetchall()]


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
