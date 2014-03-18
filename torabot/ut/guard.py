from functools import wraps
from logbook import Logger


log = Logger(__name__)


def exguard(f):
    @wraps(f)
    def g(*args, **kargs):
        try:
            return f(*args, **kargs)
        except:
            log.exception('{} failed', f.__name__)
    return g


def timeguard(f):
    from time import time

    @wraps(f)
    def g(*args, **kargs):
        start = time()
        try:
            return f(*args, **kargs)
        finally:
            log.info('{} takes {} seconds', f.__name__, time() - start)

    return g
