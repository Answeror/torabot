from datetime import datetime
from asyncio import coroutine
from logbook import Logger
from ..db import db
from . import core


log = Logger(__name__)


def query(backend, kind, text, timeout, **kargs):
    return core.mod(kind).search(text=text, timeout=timeout, backend=backend, **kargs)


@db.with_optional_bind
@coroutine
def _search(kind, text, bind, sync_on_expire=None):
    '''return None means first sync failed'''

    @coroutine
    def get_query():
        with db.connection_context(bind=bind) as conn:
            return (yield from db.get_query_bi_kind_and_text(conn, kind, text))

    @coroutine
    def sync():
        return (yield from core.sync(kind=kind, sync=sync, bind=bind))

    @coroutine
    def has():
        with db.connection_context(bind=bind) as conn:
            return (yield from db.has_filled_query_bi_kind_and_text(conn, kind, text))

    if not (yield from has()):
        log.info('query {} of {} dosn\'t exist', text, kind)
        if (yield from sync()):
            query = yield from get_query()
        else:
            query = None
    else:
        query = yield from get_query()
        if (yield from core.mod(query.kind).expired(query)):
            log.debug('query {} of {} expired', text, kind)
            if (
                (yield from core.mod(query.kind).sync_on_expire(query))
                if sync_on_expire is None
                else sync_on_expire
            ):
                if (yield from sync()):
                    query = yield from get_query()
                else:
                    log.debug(
                        'sync {} of {} timeout or meet expected error',
                        text,
                        kind
                    )
            else:
                log.debug('mark query {} of {} need sync', text, kind)
                with db.connection_context(commit=True, bind=bind) as conn:
                    yield from db.set_next_sync_time_bi_kind_and_text(
                        conn,
                        kind,
                        text,
                        datetime.utcnow()
                    )

    if query is not None and not query.result:
        raise core.CoreError('Invalid query: {}'.format(query))

    return query
