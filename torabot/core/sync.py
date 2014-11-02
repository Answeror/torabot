from datetime import datetime, timedelta
from asyncio import coroutine
from flask import current_app
from logbook import Logger
from ..db import db
from . import core


log = Logger(__name__)


@core.setattr
class SpyTimeoutError(core.CoreError):
    pass


@core.initializer
def init_app(app):
    app.config.setdefault('TORABOT_DEFAULT_SYNC_INTERVAL', 15 * 60)


@core.interface
@db.with_optional_connection(commit=True)
@coroutine
def fast_sync(kind, text, conn, timeout=None, good=None, sync_interval=None):
    root_kind, root_text = core.regular(kind, text)
    if (kind, text) == (root_kind, root_text):
        query = yield from db.get_query_bi_kind_and_text(conn, kind, text)
        return filled(query) and not expired(query)

    root = yield from db.get_query_bi_kind_and_text(conn, root_kind, root_text)
    if not filled(root):
        log.debug('root query of ({}, {}) not filled', kind, text)
        return False
    if expired(root):
        log.debug('root query of ({}, {}) expired', kind, text)
        return False
    if good and not good(root.result):
        log.debug('root query of ({}, {}) not good', kind, text)
        return False
    yield from fill_result(kind, text, root.result, sync_interval)
    return True


@core.interface
@db.with_optional_bind
@coroutine
def deep_sync(kind, text, bind, timeout=None, good=None, sync_interval=None):
    try:
        result = yield from core.mod(kind).source(text, timeout)
        if good and not good(result):
            return False
    except (core.ExpectedError, core.SpyTimeoutError) as e:
        log.debug(str(e))
        return False

    with db.connection_context(commit=True, bind=bind) as conn:
        yield from fill_result(kind, text, result, sync_interval, conn=conn)
        yield from fill_root_result(kind, text, result, sync_interval, conn=conn)
    return True


@core.interface
@db.with_optional_bind
@coroutine
def sync(*args, bind, **kargs):
    with db.connection_context(commit=True, bind=bind) as conn:
        if (yield from fast_sync(*args, conn=conn, **kargs)):
            return True

    return (yield from deep_sync(*args, **kargs))


def filled(query):
    return query is not None and query.result


def expired(query):
    return core.mod(query.kind).expired(query)


@coroutine
def fill_root_result(kind, text, result, sync_interval, conn):
    root_kind, root_text = core.regular(kind, text)
    if (kind, text) != (root_kind, root_text):
        yield from fill_result(
            root_kind,
            root_text,
            result,
            sync_interval,
            conn=conn
        )


@coroutine
def fill_result(kind, text, result, sync_interval, conn):
    query = yield from db.get_or_add_query_bi_kind_and_text(conn, kind, text)
    if query.result == result:
        yield from db.touch_query_bi_id(conn, query.id)
    else:
        yield from db.add_one_query_changes(
            conn,
            query.id,
            core.mod(kind).changes(query.result, result, query=query)
        )
        yield from db.set_query_result(conn, query.id, result)
    if (yield from db.is_query_active_bi_id(conn, query.id)):
        yield from db.set_next_sync_time(
            conn,
            query.id,
            next_sync_time(query, sync_interval)
        )
    else:
        yield from db.set_next_sync_time(conn, query.id, None)


def next_sync_time(query, sync_interval):
    return datetime.utcnow() + timedelta(seconds=(
        sync_interval
        if sync_interval is not None
        else current_app.config['TORABOT_DEFAULT_SYNC_INTERVAL']
    ))
