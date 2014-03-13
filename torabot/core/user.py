from .. import db


def get_user_id_bi_openid(openid, session):
    return db.get_user_id_bi_openid(session.connection(), openid)


def add_user(name, email, openid, session):
    return db.add_user(
        session.connection(),
        name=name,
        email=email,
        openid=openid
    )
