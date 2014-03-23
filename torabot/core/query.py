from nose.tools import assert_is_not_none, assert_equal
from datetime import datetime, timedelta
from logbook import Logger
from ..db import (
    get_query_bi_kind_and_text,
    has_query_bi_kind_and_text,
    get_query_mtime_bi_kind_and_text,
)
from .sync import sync
from .local import get_current_conf


log = Logger(__name__)


def from_remote(conn, kind, text):
    return get_query_bi_kind_and_text(conn, kind, text)


def has(conn, kind, text):
    return has_query_bi_kind_and_text(conn, kind, text)


def expired(conn, kind, text):
    mtime = get_query_mtime_bi_kind_and_text(conn, kind, text)
    assert_is_not_none(mtime)
    return mtime + timedelta(seconds=interval()) < datetime.utcnow()


def interval():
    t = get_current_conf()['TORABOT_QUERY_EXPIRE']
    assert_equal(int(t), t)
    return int(t)


def query(conn, kind, text, timeout):
    dosync = lambda: sync(kind, text, timeout, conn=conn)
    if not has(conn, kind, text):
        log.info('query {} of {} dosn\'t exist', text, kind)
        dosync()
    elif expired(conn, kind, text):
        log.info('query {} of {} expired', text, kind)
        dosync()
    return get_query_bi_kind_and_text(conn, kind, text)
