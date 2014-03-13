from functools import wraps
from flask import session, redirect, url_for


def require_session(f):
    @wraps(f)
    def inner(*args, **kargs):
        user_id = session.get('userid')
        if user_id is None:
            return redirect(url_for('index'))
        return f(*args, user_id=user_id, **kargs)

    return inner
