from functools import wraps
from flask import session
from .errors import AuthError
from ..core.user import get_user_id_bi_openid


def require_session(f):
    @wraps(f)
    def inner(*args, **kargs):
        openid = session.get('openid')
        if openid is None:
            raise AuthError()
        return f(*args, user_id=get_user_id_bi_openid(openid), **kargs)

    return inner
