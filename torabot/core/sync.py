from datetime import datetime, timedelta
from .local import get_current_conf
from .mod import mod
from ..mods.errors import ExpectedError, SpyTimeoutError
from logbook import Logger


log = Logger(__name__)


def sync(backend, kind, text, timeout, good=None, sync_interval=None):
    try:
        result = mod(kind).spy(text, timeout)
        if good and not good(result):
            return False
    except (ExpectedError, SpyTimeoutError) as e:
        log.debug(str(e))
        return False

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

    return True


def next_sync_time(query, sync_interval):
    return datetime.utcnow() + timedelta(seconds=(
        sync_interval if sync_interval is not None
        else get_current_conf()['TORABOT_DEFAULT_SYNC_INTERVAL']
    ))
