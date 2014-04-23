from functools import wraps
from flask import session
from .errors import AuthError


def require_session(f):
    @wraps(f)
    def inner(*args, **kargs):
        user_id = session.get('userid')
        if user_id is None:
            raise AuthError()
        return f(*args, user_id=user_id, **kargs)

    return inner
