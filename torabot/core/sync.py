'''
model used to sync tora and local database
'''


from logbook import Logger
from fn.iters import head
from ..ut.session import sessionguard
from ..ut.bunch import Bunch
from ..db import (
    set_results,
    set_total,
    put_query,
    get_query_bi_text,
    get_arts_bi_query_id,
    put_art,
    get_art_bi_uri,
    get_art_hash_bi_uri,
)


log = Logger(__name__)


def strict(query, n, spider, makesession):
    log.info('start sync %s %d' % (query, n))
    ret = list(lazy(
        query,
        n,
        spider,
        makesession=makesession,
    ))
    log.info('done sync %s %d' % (query, n))
    return ret


def synced_from_head(query, n, spider, makesession):
    return synced_on(query, 0, spider, makesession) and synced_on(query, n - 1, spider, makesession)


def synced_on(query, n, spider, makesession):
    with sessionguard(make=makesession) as session:
        local = art_n_from_db(query.id, n, session.connection())

    if local is None:
        return False
    remote = spider.art_n(query.text, n)
    if remote is None:
        return False
    return same_art(local, Bunch(**remote))


def art_n_from_db(query_id, n, makesession):
    return head(get_arts_bi_query_id(
        makesession,
        query_id,
        offset=n,
        limit=1,
    ))


def lazy(query, n, spider, makesession):
    if isinstance(query, str):
        with sessionguard(make=makesession, commit=True) as session:
            put_query(session.connection(), query)
            query = get_query_bi_text(session.connection(), query)

    if synced_from_head(query, n, spider, makesession):
        with sessionguard(make=makesession, commit=True) as session:
            arts = get_arts_bi_query_id(
                session.connection(),
                query.id,
                offset=0,
                limit=n,
            )
        yield from arts
        return

    yield from pull_from_head(query, n, spider, makesession)


def pull_from_head(query, n, spider, makesession):
    ds = iter(list(spider.gen_arts_from_head(query.text, n, return_total=True)))
    with sessionguard(make=makesession, commit=True) as session:
        conn = session.connection()
        set_total(conn, id=query.id, total=next(ds))
        arts = []
        for rank, art in enumerate(ds):
            art = Bunch(**art)
            if art.hash != get_art_hash_bi_uri(conn, art.uri):
                put_art(conn, uri=art.uri, params=art)
            arts.append(get_art_bi_uri(conn, art.uri))
        set_results(conn, query_id=query.id, art_ids=[art.id for art in arts])
    return arts


def same_art(lhs, rhs):
    return lhs.uri == rhs.uri and lhs.hash == rhs.hash
