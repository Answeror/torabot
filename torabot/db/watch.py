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
