from functools import wraps
import sqlalchemy.exc


class DBError(Exception):
    pass


class InvalidArgumentError(DBError):
    pass


class UniqueConstraintError(DBError):
    pass


def error_guard(f):
    @wraps(f)
    def inner(*args, **kargs):
        try:
            return f(*args, **kargs)
        except sqlalchemy.exc.DataError as e:
            raise InvalidArgumentError from e
        except sqlalchemy.exc.IntegrityError as e:
            if 'duplicate' in str(e):
                raise UniqueConstraintError from e
            raise
    return inner
