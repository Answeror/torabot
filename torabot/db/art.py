from ..ut.bunch import Bunch


def add_art(
    conn,
    title,
    author,
    company,
    uri,
    status,
    hash,
):
    ret = conn.execute((
        'insert into art (title, author, company, uri, status, hash) '
        'values (%s, %s, %s, %s, %s, %s) '
        'returning *'
    ), (title, author, company, uri, status, hash)).fetchone()
    return ret[0]


def put_art(conn, params, **conditions):
    keys = [key for key in params]
    d = dict(**conditions)
    d.update(params)
    condition_string = ' and '.join('%s = %%(%s)s' % (key, key) for key in conditions)
    conn.execute(''.join([
        'update art set %s ' % ', '.join('%s = %%(%s)s' % (key, key) for key in keys),
        'where %s' % condition_string
    ]), d)
    conn.execute(''.join([
        'insert into art (%s) ' % ', '.join(keys),
        'select %s ' % ', '.join('%%(%s)s' % key for key in keys),
        'where not exists (select 1 from art where %s)' % condition_string
    ]), d)


def art_count(conn):
    return conn.execute('select count(*) from art').fetchone()[0]


def get_art_bi_uri(conn, uri):
    ret = conn.execute((
        'select * from art '
        'where uri = %s'
    ), (uri,)).fetchone()
    return None if ret is None else Bunch(**ret)
