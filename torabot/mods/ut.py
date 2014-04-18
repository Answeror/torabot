import sh
from functools import wraps


def check_scrapyd():
    if 'scrapyd' not in sh.ps('cax'):
        raise RuntimeError('scrapyd not running')


def need_scrapyd(f):
    @wraps(f)
    def g(*args, **kargs):
        check_scrapyd()
        return f(*args, **kargs)
    return g
