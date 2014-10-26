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
