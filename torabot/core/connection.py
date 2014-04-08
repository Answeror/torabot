from contextlib import contextmanager
from ..ut.connection import ccontext, appccontext
from ..ut.engine import appengine
from .local import get_current_conf


@contextmanager
def autoccontext(commit=False, **kargs):
    try:
        kargs.update(engine=appengine())
    except:
        kargs.update(config=get_current_conf())
    with ccontext(commit=commit, **kargs) as conn:
        yield conn
