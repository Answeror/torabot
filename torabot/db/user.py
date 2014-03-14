def add_user(conn, name, email, openid):
    return conn.execute((
        'insert into "user" (name, email, openid)'
        'values (%s, %s, %s) '
        'returning *'
    ), (name, email, openid)).fetchone()[0]


def get_user_id_bi_openid(conn, openid):
    ret = conn.execute('select id from "user" where openid = %s', (openid,)).fetchone()
    return None if ret is None else ret[0]


def get_user_email_bi_id(conn, id):
    ret = conn.execute('select email from "user" where id = %s', (id,)).fetchone()
    return None if ret is None else ret[0]
