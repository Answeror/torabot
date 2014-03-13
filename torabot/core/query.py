from logbook import Logger
from nose.tools import assert_less_equal
from ..db.query import (
    get_query_bi_text,
    has_query_bi_text,
    get_arts_bi_query_id,
)
from .sync import strict
from .const import SYNC_LIMIT


log = Logger(__name__)


def get_query_text_from_kargs(kargs):
    if 'query_text' in kargs:
        return kargs['query_text']
    if 'query' in kargs:
        return kargs['query'].text
    assert False, 'neither query_text nor query provided'


def get_query_from_kargs(conn, kargs):
    if 'query' in kargs:
        return kargs['query']
    return get_query_bi_text(conn, get_query_text_from_kargs(kargs))


def from_remote(begin, end, conn, spider, return_query=False, **kargs):
    text = get_query_text_from_kargs(kargs)
    strict(
        text,
        n=SYNC_LIMIT if end is None else end,
        spider=spider,
        conn=conn,
    )
    query = get_query_from_kargs(conn, kargs)
    arts = get_arts_bi_query_id(
        conn,
        query_id=query.id,
        offset=begin,
        **({} if end is None else {'limit': end - begin})
    )
    return arts if not return_query else (arts, query)


def check_range(begin, end):
    if end is not None:
        assert_less_equal(begin, end)


def query(text, spider, conn, begin=0, end=None, return_detail=False):
    check_range(begin, end)

    log.debug('query {} in ({}, {})', text, begin, end)
    if not has_query_bi_text(conn, text):
        arts, query = from_remote(
            query_text=text,
            begin=begin,
            end=end,
            return_query=True,
            spider=spider,
            conn=conn
        )
    else:
        log.debug('{} already synced, pull from database')
        query = get_query_bi_text(conn, text)
        arts = from_db_and_remote(query, begin, end, spider, conn)

    return arts if not return_detail else {
        'arts': arts,
        'total': query.total
    }


def not_enough(begin, end, arts):
    return end is None or begin + len(arts) < end


def has_more(begin, query, arts):
    return begin + len(arts) < query.total


def from_db_and_remote(query, begin, end, spider, conn):
    arts = get_arts_bi_query_id(
        conn,
        query_id=query.id,
        offset=begin,
        **({} if end is None else {'limit': end - begin})
    )
    if not_enough(begin, end, arts) and has_more(begin, query, arts):
        return from_remote(
            query=query,
            begin=begin,
            end=end,
            spider=spider,
            conn=conn,
        )
    return arts
