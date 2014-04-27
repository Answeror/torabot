from functools import wraps
from ...core.local import is_admin
from ..auth import require_session
from .errors import AdminAuthError


def require_admin(f):
    @require_session
    @wraps(f)
    def inner(user_id, *args, **kargs):
        if not is_admin:
            raise AdminAuthError()
        return f(*args, **kargs)

    return inner
