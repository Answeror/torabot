'''
model used to sync tora and local database
'''


from sqlalchemy.sql import exists, and_, select, insert, delete
from sqlalchemy import event
from logbook import Logger
from nose.tools import assert_is_not_none
from fn.iters import head
from .model import Art, Change, Query, Result
from .redis import redis
from .time import utcnow


log = Logger(__name__)


def dict_to_art(d):
    art = Art(
        title=d['title'],
        author=d['author'],
        company=d['company'],
        state=Art.RESERVE if d['reserve'] else Art.OTHER,
        ptime=d['ptime'],
        hash=d['hash'],
    )
    art.uri = d['uri']
    return art


def art_new(art, session):
    return not bool(session.query(exists().where(
        Art.toraid == art.toraid
    )).scalar())


def art_changed(art, session):
    return not bool(session.query(exists().where(and_(
        Art.toraid == art.toraid,
        Art.hash == art.hash
    ))).scalar())


def update_art(art, session):
    old = session.query(Art).filter_by(toraid=art.toraid).one()
    if art.reserve and not old.reserve:
        add_reserve_change(old, session)
    art.id = old.id
    art = session.merge(art)
    session.flush()
    return art


def broadcast_change(*args, **kargs):
    redis.rpush('change', None)


def add_reserve_change(art, session):
    session.add(Change(art=art, what=Change.RESERVE))
    event.listen(session, 'after_commit', broadcast_change)


def add_new_change(art, session):
    session.add(Change(art=art, what=Change.NEW, ctime=art.atime))
    event.listen(session, 'after_commit', broadcast_change)


def has_query(session, **kargs):
    if 'query' in kargs:
        query = kargs['query']
    elif 'text' in kargs:
        query = Query(text=kargs['text'])
    else:
        assert False, 'must provide query or text'
    return bool(session.query(
        exists()
        .where(Query.text == query.text)
    ).scalar())


def put_query(text, session):
    if has_query(text=text, session=session):
        return session.query(Query).filter_by(text=text).one()
    query = Query(text=text)
    session.add(query)
    session.flush()
    session.expire(query, ['id'])
    return query


def add_art(art, query, rank, session):
    art.atime = utcnow()
    add_new_change(art, session)
    session.add(art)


def add_query_result(query, art, rank, session):
    assert_is_not_none(art.id)
    assert_is_not_none(query.id)
    session.execute(
        insert(Result)
        .values(
            query_id=query.id,
            art_id=art.id,
            rank=rank,
        )
    )


def clear_query_result(query, session):
    session.execute(
        delete(Result)
        .where(Result.query_id == query.id)
    )


def sync(query, n, spider, session):
    return list(lazy(
        query,
        n,
        spider,
        session=session,
    ))


def synced_from_head(query, n, spider, session):
    return synced_on(query, 0, spider, session) and synced_on(query, n - 1, spider, session)


def synced_on(query, n, spider, session):
    art = art_n_from_db(query.id, n, session)
    if art is None:
        return False
    d = spider.art_n(query.text, n)
    if d is None:
        return False
    return same_art(art, dict_to_art(d))


def art_n_from_db(query_id, n, session):
    return head(arts_from_db(
        query_id,
        offset=n,
        limit=1,
        session=session,
    ))


def arts_from_db(query_id, offset, limit, session):
    idq = (
        select([Result.art_id.label('id'), Result.rank])
        .where(Result.query_id == query_id)
        .order_by(Result.rank)
        .offset(offset)
        .limit(limit)
        .alias()
    )
    return (
        session.query(Art)
        .join(idq, Art.id == idq.c.id)
        .order_by(idq.c.rank)
        .all()
    )


def lazy(query, n, spider, session):
    if isinstance(query, str):
        query = put_query(query, session)

    if synced_from_head(query, n, spider, session):
        yield from arts_from_db(
            query.id,
            offset=0,
            limit=n,
            session=session
        )
        return

    yield from pull_from_head(query, n, spider, session)


def art_from_db_bi_toraid(toraid, session):
    return session.query(Art).filter_by(toraid=toraid).one()


def pull_from_head(query, n, spider, session):
    clear_query_result(query, session)
    for rank, art in enumerate(map(
        dict_to_art,
        spider.gen_arts_from_head(query.text, n)
    )):
        if art_new(art, session):
            add_art(art, query, rank, session)
            session.flush()
            session.expire(art, ['id'])
        elif art_changed(art, session):
            art = update_art(art, session)
        else:
            art = art_from_db_bi_toraid(art.toraid, session)
        add_query_result(query, art, rank, session)
        yield art


def same_art(lhs, rhs):
    return lhs.toraid == rhs.toraid and lhs.hash == rhs.hash
