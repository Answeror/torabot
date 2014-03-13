from ..ut.bunch import Bunch


def add_art(
    conn,
    title,
    author,
    company,
    toraid,
    status,
    hash,
):
    ret = conn.execute((
        'insert into art (title, author, company, toraid, status, hash) '
        'values (%s, %s, %s, %s, %s, %s) '
        'returning *'
    ), (title, author, company, toraid, status, hash)).fetchone()
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


def get_art_bi_toraid(conn, toraid):
    ret = conn.execute((
        'select title, author, company, toraid, status, hash '
        'from art '
        'where toraid=%s'
    ), (toraid,)).fetchone()
    return None if ret is None else Bunch(**ret)
