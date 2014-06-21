from flask import current_app
from itsdangerous import(
    TimedJSONWebSignatureSerializer as Serializer,
    SignatureExpired,
    BadSignature
)
from ... import db
from ...core.connection import autoccontext


def check_token(token):
    if not token:
        return False
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return False  # valid token, but expired
    except BadSignature:
        return False  # invalid token
    with autoccontext() as conn:
        return db.has_user_bi_id(conn, data.get('id'))


def make_token(user, expiration=600):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'id': user.id}).decode('ascii')
