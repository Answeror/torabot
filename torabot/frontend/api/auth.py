from functools import wraps
from ...core.local import request_values
from .errors import InvalidTokenError
from .token import check_token


def token_required(f):
    @wraps(f)
    def inner(*args, **kargs):
        if not check_token(request_values.get('token')):
            raise InvalidTokenError(request_values.get('token'))
        return f(*args, **kargs)

    return inner
