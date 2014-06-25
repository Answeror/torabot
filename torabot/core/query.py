from datetime import datetime
from logbook import Logger
from ..db import (
    get_query_bi_kind_and_text,
    has_query_bi_kind_and_text,
    set_next_sync_time_bi_kind_and_text,
)
from .sync import sync
from .mod import mod


log = Logger(__name__)


def from_remote(conn, kind, text):
    return get_query_bi_kind_and_text(conn, kind, text)


def has(conn, kind, text):
    return has_query_bi_kind_and_text(conn, kind, text)


def query(conn, kind, text, timeout):
    return mod(kind).search(text=text, timeout=timeout, conn=conn)


def search_from_redis(kind, text, timeout):
    pass


def search_from_db(conn, kind, text, timeout):
    '''return None means first sync failed'''
    if not has(conn, kind, text):
        log.info('query {} of {} dosn\'t exist', text, kind)
        if sync(kind, text, timeout, conn=conn):
            query = get_query_bi_kind_and_text(conn, kind, text)
        else:
            query = None
    else:
        query = get_query_bi_kind_and_text(conn, kind, text)
        if mod(query.kind).expired(query):
            log.debug('query {} of {} expired', text, kind)
            if mod(query.kind).sync_on_expire(query):
                if not sync(kind, text, timeout, conn=conn):
                    log.debug('sync {} of {} timeout or meet expected error', text, kind)
                query = get_query_bi_kind_and_text(conn, kind, text)
            else:
                mark_need_sync(conn, kind, text)
    return query


def mark_need_sync(conn, kind, text):
    log.debug('mark query {} of {} need sync', text, kind)
    set_next_sync_time_bi_kind_and_text(conn, kind, text, datetime.utcnow())
