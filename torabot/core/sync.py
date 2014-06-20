from contextlib import contextmanager
from datetime import datetime, timedelta
from ..ut.connection import ccontext
from ..db import (
    get_or_add_query_bi_kind_and_text,
    add_one_query_changes,
    set_query_result,
    touch_query_bi_id,
    set_next_sync_time,
    is_query_active_bi_id,
)
from .local import get_current_conf
from .mod import mod
from ..mods.errors import ExpectedError, SpyTimeoutError
from logbook import Logger


log = Logger(__name__)


def sync(kind, text, timeout, sync_interval=None, **kargs):
    try:
        result = mod(kind).spy(text, timeout)
    except (ExpectedError, SpyTimeoutError) as e:
        log.debug(str(e))
        return

    with context(**kargs) as conn:
        query = get_or_add_query_bi_kind_and_text(conn, kind, text)
        if query.result == result:
            touch_query_bi_id(conn, query.id)
        else:
            add_one_query_changes(
                conn,
                query.id,
                mod(kind).changes(query.result, result)
            )
            set_query_result(conn, query.id, result)
        if is_query_active_bi_id(conn, query.id):
            set_next_sync_time(conn, query.id, next_sync_time(query, sync_interval))
        else:
            set_next_sync_time(conn, query.id, None)


def next_sync_time(query, sync_interval):
    return datetime.utcnow() + timedelta(seconds=(
        sync_interval if sync_interval is not None
        else get_current_conf()['TORABOT_DEFAULT_SYNC_INTERVAL']
    ))


@contextmanager
def context(**kargs):
    if 'conn' in kargs:
        yield kargs['conn']
    elif 'engine' in kargs:
        with ccontext(commit=True, engine=kargs['engine']) as conn:
            yield conn
    else:
        assert False, 'must provide conn or engine'
