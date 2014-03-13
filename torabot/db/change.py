def has_change(conn):
    return conn.execute('select * from change').fetchone() is not None


def has_change_bi_art_id(conn, art_id):
    return conn.execute((
        'select * from change '
        'where art_id = %s '
    ), (art_id,)).fetchone() is not None


def change_count_bi_art_id(conn, art_id):
    return conn.execute((
        'select count(*) from change '
        'where art_id = %s '
    ), (art_id,)).fetchone()[0]
