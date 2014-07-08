from datetime import datetime, timedelta
from .local import get_current_conf
from .mod import mod
from ..mods.errors import ExpectedError, SpyTimeoutError
from logbook import Logger


log = Logger(__name__)


def fast_sync(backend, kind, text, timeout, good=None, sync_interval=None):
    root_kind, root_text = regular(kind, text)
    if (kind, text) == (root_kind, root_text):
        return False
    root = backend.get_query_bi_kind_and_text(kind, text)
    if not filled(root) or expired(root) or (good and not good(root.result)):
        return False
    fill_result(backend, kind, text, root.result, sync_interval)
    return True


def filled(query):
    return query is not None and query.result


def expired(query):
    return mod(query.kind).expired(query)


def sync(backend, kind, text, timeout, good=None, sync_interval=None):
    try:
        result = mod(kind).spy(text, timeout)
        if good and not good(result):
            return False
    except (ExpectedError, SpyTimeoutError) as e:
        log.debug(str(e))
        return False

    fill_result(backend, kind, text, result, sync_interval)
    fill_root_result(backend, kind, text, result, sync_interval)
    return True


def fill_root_result(backend, kind, text, result, sync_interval):
    root_kind, root_text = regular(kind, text)
    if (kind, text) != (root_kind, root_text):
        fill_result(backend, root_kind, root_text, result, sync_interval)


def fill_result(backend, kind, text, result, sync_interval):
    query = backend.get_or_add_query_bi_kind_and_text(kind, text)
    if query.result == result:
        backend.touch_query_bi_id(query.id)
    else:
        backend.add_one_query_changes(
            query.id,
            mod(kind).changes(query.result, result)
        )
        backend.set_query_result(query.id, result)
    if backend.is_query_active_bi_id(query.id):
        backend.set_next_sync_time(query.id, next_sync_time(query, sync_interval))
    else:
        backend.set_next_sync_time(query.id, None)


def next_sync_time(query, sync_interval):
    return datetime.utcnow() + timedelta(seconds=(
        sync_interval if sync_interval is not None
        else get_current_conf()['TORABOT_DEFAULT_SYNC_INTERVAL']
    ))


def regular(kind, text):
    while True:
        next_kind, next_text = mod(kind).regular(text)
        if (next_kind, next_text) == (kind, text):
            break
        kind, text = next_kind, next_text
    return kind, text
