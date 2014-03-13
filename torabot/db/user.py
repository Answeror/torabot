

def add_user(
    conn,
    name,
    email,
    openid,
):
    ret = conn.execute((
        'insert into "user" (name, email, openid)'
        'values (%s, %s, %s) '
        'returning *'
    ), (name, email, openid)).fetchone()
    return ret[0]
