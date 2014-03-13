def watch(conn, user_id, query_id):
    conn.execute((
        'insert into watch (user_id, query_id) '
        'select %(user_id)s, %(query_id)s '
        'where not exists (select 1 from watch '
        'where user_id = %(user_id)s and query_id = %(query_id)s)'
    ), dict(user_id=user_id, query_id=query_id))
