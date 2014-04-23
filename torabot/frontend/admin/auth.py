from functools import wraps
from flask import current_app
from ..auth import require_session
from .errors import AdminAuthError


def require_admin(f):
    @require_session
    @wraps(f)
    def inner(user_id, *args, **kargs):
        if user_id not in current_app.config['TORABOT_ADMIN_IDS']:
            raise AdminAuthError()
        return f(*args, **kargs)

    return inner
