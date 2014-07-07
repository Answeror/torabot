from functools import partial
from datetime import datetime
from logbook import Logger
from .sync import sync
from .mod import mod


log = Logger(__name__)


def has(backend, kind, text):
    return backend.has_query_bi_kind_and_text(kind, text)


def query(backend, kind, text, timeout, **kargs):
    return mod(kind).search(text=text, timeout=timeout, backend=backend, **kargs)


def _search(backend, kind, text, timeout, sync_on_expire=None, **kargs):
    '''return None means first sync failed'''
    sync_options = {key: kargs[key] for key in kargs if key in [
        'good',
        'sync_interval'
    ]}
    _sync = partial(
        sync,
        kind=kind,
        text=text,
        timeout=timeout,
        backend=backend,
        **sync_options
    )
    get_query = partial(
        backend.get_query_bi_kind_and_text,
        kind=kind,
        text=text
    )
    if not has(backend, kind, text):
        log.info('query {} of {} dosn\'t exist', text, kind)
        if _sync():
            query = get_query()
        else:
            query = None
    else:
        query = get_query()
        if mod(query.kind).expired(query):
            log.debug('query {} of {} expired', text, kind)
            if (
                mod(query.kind).sync_on_expire(query) if sync_on_expire is None
                else sync_on_expire
            ):
                if _sync():
                    query = get_query()
                else:
                    log.debug(
                        'sync {} of {} timeout or meet expected error',
                        text,
                        kind
                    )
            else:
                mark_need_sync(backend, kind, text)
    return query


def mark_need_sync(backend, kind, text):
    log.debug('mark query {} of {} need sync', text, kind)
    backend.set_next_sync_time_bi_kind_and_text(kind, text, datetime.utcnow())


def regular(kind, text):
    while True:
        next_kind, next_text = mod(kind).regular(text)
        if (next_kind, next_text) == (kind, text):
            break
        kind, text = next_kind, next_text
    return kind, text
