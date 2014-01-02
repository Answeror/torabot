from functools import wraps
from logbook import Logger


log = Logger(__name__)


def exception_guard(f):
    @wraps(f)
    def inner(*args, **kargs):
        try:
            return f(*args, **kargs)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            log.exception('caught by exception guard')

    return inner
