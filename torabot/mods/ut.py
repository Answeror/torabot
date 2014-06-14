import sh
from functools import wraps
from nose.tools import assert_is_not_none
from .. import make
from ..core.mod import mod


def check_scrapyd():
    if 'scrapyd' not in sh.ps('cax'):
        raise RuntimeError('scrapyd not running')


def need_scrapyd(f):
    @wraps(f)
    def g(*args, **kargs):
        check_scrapyd()
        return f(*args, **kargs)
    return g


def check_format_notice_body_not_none(name, view, notice):
    app = make()
    with app.app_context():
        assert_is_not_none(mod(name).format_notice_body(view, notice))


def check_format_notice_body_not_empty(name, view, notice):
    app = make()
    with app.app_context():
        assert mod(name).format_notice_body(view, notice)
