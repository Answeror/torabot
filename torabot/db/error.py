from functools import wraps
import sqlalchemy.exc


class InvalidArgumentError(Exception):
    pass


def error_guard(f):
    @wraps(f)
    def inner(*args, **kargs):
        try:
            return f(*args, **kargs)
        except sqlalchemy.exc.DataError as e:
            raise InvalidArgumentError from e
    return inner
