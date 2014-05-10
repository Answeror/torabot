from contextlib import contextmanager
from ..ut.connection import ccontext, appccontext
assert appccontext
from ..ut.engine import appengine


@contextmanager
def autoccontext(commit=False, **kargs):
    try:
        kargs.update(engine=appengine())
    except:
        from .local import get_current_conf
        kargs.update(config=get_current_conf())
    with ccontext(commit=commit, **kargs) as conn:
        yield conn
