

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


def put_art(conn, id, **kargs):
    keys = [key for key in kargs]
    params = dict(**kargs)
    params['id'] = id
    conn.execute(''.join([
        'update art set %s ' % ', '.join('%s = %%(%s)s' % (key, key) for key in keys),
        'where id = %(id)s'
    ]), params)
    conn.execute(''.join([
        'insert into art (%s) ' % ', '.join(keys),
        'select %s ' % ', '.join('%%(%s)s' % key for key in keys),
        'where not exists (select 1 from art where id = %(id)s)'
    ]), params)
