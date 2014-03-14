'''
model used to sync tora and local database
'''


from logbook import Logger
from fn.iters import head
from ..ut.bunch import Bunch
from ..db import (
    set_results,
    set_total,
    put_query,
    get_query_bi_text,
    get_arts_bi_query_id,
    put_art,
    get_art_bi_uri,
)


log = Logger(__name__)


def strict(query, n, spider, conn):
    log.info('start sync %s %d' % (query, n))
    ret = list(lazy(
        query,
        n,
        spider,
        conn=conn,
    ))
    log.info('done sync %s %d' % (query, n))
    return ret


def synced_from_head(query, n, spider, conn):
    return synced_on(query, 0, spider, conn) and synced_on(query, n - 1, spider, conn)


def synced_on(query, n, spider, conn):
    local = art_n_from_db(query.id, n, conn)
    if local is None:
        return False
    remote = spider.art_n(query.text, n)
    if remote is None:
        return False
    return same_art(local, Bunch(**remote))


def art_n_from_db(query_id, n, conn):
    return head(get_arts_bi_query_id(
        conn,
        query_id,
        offset=n,
        limit=1,
    ))


def lazy(query, n, spider, conn):
    if isinstance(query, str):
        put_query(conn, query)
        query = get_query_bi_text(conn, query)

    if synced_from_head(query, n, spider, conn):
        yield from get_arts_bi_query_id(
            conn,
            query.id,
            offset=0,
            limit=n,
        )
        return

    yield from pull_from_head(query, n, spider, conn)


def pull_from_head(query, n, spider, conn):
    ds = spider.gen_arts_from_head(query.text, n, return_total=True)
    set_total(conn, id=query.id, total=next(ds))
    arts = []
    for rank, art in enumerate(ds):
        art = Bunch(**art)
        put_art(conn, uri=art.uri, params=art)
        arts.append(get_art_bi_uri(conn, art.uri))
    set_results(conn, query_id=query.id, art_ids=[art.id for art in arts])
    return arts


def same_art(lhs, rhs):
    return lhs.uri == rhs.uri and lhs.hash == rhs.hash
