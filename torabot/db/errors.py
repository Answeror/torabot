from functools import wraps
import sqlalchemy.exc


class DBError(Exception):
    pass


class UserNotExistError(DBError):
    pass


class EmailNotExistError(DBError):
    pass


class InvalidArgumentError(DBError):
    pass


class InvalidEmailError(DBError):
    pass


class UniqueConstraintError(DBError):
    pass


class DeleteMainEmainError(DBError):
    pass


class EmailCountLimitError(DBError):
    pass


class DeleteEmailInUseError(DBError):
    pass


class WatchCountLimitError(DBError):
    pass


def error_guard(f):
    @wraps(f)
    def inner(conn, *args, **kargs):
        try:
            return f(conn, *args, **kargs)
        except sqlalchemy.exc.DataError as e:
            raise InvalidArgumentError from e
        except sqlalchemy.exc.IntegrityError as e:
            if 'duplicate' in str(e):
                raise UniqueConstraintError(str(e)) from e
            if 'update or delete on table "email" violates foreign key constraint "watch_email_id_fkey" on table "watch"' in str(e):
                raise DeleteEmailInUseError from e
            raise
        except sqlalchemy.exc.InternalError as e:
            if 'cannot delete main email of' in str(e):
                raise DeleteMainEmainError from e
            if 'email count reach limit' in str(e):
                raise EmailCountLimitError from e
            if 'watch count reach limit' in str(e):
                raise WatchCountLimitError from e
            raise
    return inner
