from functools import wraps
from logbook import Logger


log = Logger(__name__)


def exception_guard(f):
    @wraps(f)
    def g(*args, **kargs):
        try:
            return f(*args, **kargs)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            log.exception('{} failure caught by exception guard', f.__name__)
    return g
