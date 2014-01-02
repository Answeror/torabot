'''
model used to sync tora and local database
'''


from .model import Art, Change, Query, Result
from .spider import list_all, ROOM
from sqlalchemy.sql import exists, and_, func, update, select, insert, desc
from sqlalchemy import event
from . import state
from . import what
from logbook import Logger
from fn.iters import take, head, drop
from nose.tools import assert_equal, assert_less_equal
from .redis import redis


log = Logger(__name__)


def dict_to_art(d):
    art = Art(
        title=d['title'],
        author=d['author'],
        comp=d['comp'],
        state=state.RESERVE if d['reserve'] else state.OTHER,
        ptime=d['ptime'],
        hash=d['hash'],
    )
    art.uri = d['uri']
    return art


def isnew(art, session):
    return not bool(session.query(exists().where(
        Art.toraid == art.toraid
    )).scalar())


def isreserve(art, session):
    return art.reserve and not bool(session.query(exists().where(and_(
        Art.toraid == art.toraid,
        Art.state == state.RESERVE
    ))).scalar())


def query_result_changed(query_id, art, session):
    return not bool(session.query(exists().where(and_(
        Result.query_id == query_id,
        Result.hash == art.hash
    ))).scalar())


def art_changed(art, session):
    return not bool(session.query(exists().where(and_(
        Art.toraid == art.toraid,
        Art.hash == art.hash
    ))).scalar())


def has_art(art, session):
    return bool(session.query(
        exists()
        .where(Art.toraid == art.toraid)
    ).scalar())


def update_art(art, session):
    art.id = session.query(Art).filter_by(toraid=art.toraid).one().id
    art = session.merge(art)
    session.flush()
    return art


def broadcast_change(*args, **kargs):
    redis.rpush('change', None)


def add_reserve_change(art, session):
    session.add(Change(art=art, what=what.RESERVE))
    event.listen(session, 'after_commit', broadcast_change)


def add_new_change(art, session):
    session.add(Change(art=art, what=what.NEW))
    event.listen(session, 'after_commit', broadcast_change)


def checkstate(art, session):
    return (
        isreserve(art, session),
        isnew(art, session),
    )


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
        query = session.query(Query).filter_by(text=text).one()
        query.version += 1
        session.flush()
        return query
    query = Query(text=text)
    session.add(query)
    session.flush()
    session.expire(query, ['id'])
    return query


def add_art(art, query, begin, session):
    add_new_change(art, session)
    session.add(art)
    session.flush()
    session.expire(art, ['id'])
    assert art.id is not None
    assert query.id is not None
    session.execute(
        insert(Result)
        .values(
            query_id=query.id,
            art_id=art.id,
            version=query.version,
            hash=art.hash,
            rank=next_rank_stmt(query, begin)
        )
    )


def next_rank_stmt(query, begin):
    sub = (
        select([Result.rank])
        .where(and_(
            Result.query_id == query.id,
            Result.version == query.version
        ))
        .correlate()
        .union(select([begin - 1]))
        .alias()
    )
    return (
        select([func.max(sub.c.rank) + 1])
        .as_scalar()
    )


def update_query_result(query, art, begin, session):
    session.execute(
        update(Result)
        .where(and_(
            Result.query_id == query.id,
            Result.art_id == art.id
        ))
        .values(
            version=query.version,
            hash=art.hash,
            rank=next_rank_stmt(query, begin)
        )
    )


def sync(query, session, begin=0, end=None, limit=1024):
    return list(gensync(
        query,
        begin=begin,
        end=end,
        limit=limit,
        session=session,
    ))


def promote_left(query, n, session):
    if n == 0:
        return

    results = (
        session
        .query(Result)
        .filter_by(query_id=query.id)
        .order_by(desc(Result.version), Result.rank)
        .limit(n)
        .all()
    )
    for rank, result in enumerate(results):
        result.version = query.version
        result.rank = rank
    session.flush()


def gensync(query, session, begin=0, end=None, limit=1024):
    log.debug('sync start: {}', query)
    count = 0
    for art in _gensync(put_query(query, session), begin, end, limit, session):
        count += 1
        yield art
    log.debug('sync done, update {} arts', count)


def optional_limit(stmt, begin, end):
    return stmt if end is None else stmt.limit(end - begin)


def clear_hash(query, begin, end, session):
    check_range(begin, end)
    session.execute(
        update(Result)
        .where(Result.query_id.in_(optional_limit((
            select([Result.query_id])
            .where(Result.query_id == query.id)
            .order_by(desc(Result.version), Result.rank)
            .offset(begin)
        ), begin, end)))
        .values(hash=None)
    )


def get_arts_from_remote(query_text, begin):
    yield from map(dict_to_art, list_all(query_text, begin=begin))


def find_sync_begin_point(query, begin, end, session):
    if not remote_no_change_at(query, begin, session):
        return 0

    span = ROOM // 2
    while begin + span < end:
        mid = (begin + end) // 2
        if remote_no_change_at(query, mid, session):
            begin = mid + 1
        else:
            end = mid

    return begin


def _gensync(query, begin, end, limit, session):
    if not remote_no_change(query, 0, begin, session):
        next_begin = find_sync_begin_point(query, 0, begin, session)
        log.debug('left of {} changed, sync from {}', begin, next_begin)
        yield from drop(begin, _gensync(
            query=query,
            begin=next_begin,
            end=end,
            limit=limit,
            session=session
        ))
        return

    if not remote_no_change(query, begin, end, session):
        log.debug('[{}, {}) changed, clear result hash', begin, end)
        clear_hash(query, begin, end, session)

    promote_left(query, begin, session)

    ret = list_all(query.text, begin=begin, return_total=True)
    query.total = next(ret)

    arts = map(dict_to_art, ret)
    for turn, art in zip(
        range(limit + 1),
        arts if end is None else take(end - begin, arts)
    ):
        if turn == limit:
            log.info('sync limit({}) reached for query {}', limit, query.text)
            break

        isreserve, isnew = checkstate(art, session)
        if isreserve:
            add_reserve_change(art, session)
        if isnew:
            add_art(art, query, begin, session)
        else:
            if art_changed(art, session):
                art = update_art(art, session)
            if query_result_changed(query.id, art, session):
                update_query_result(query, art, begin, session)
            else:
                log.debug('{} unchange', art.toraid)
                break
        yield art


def min_rank(query, session):
    ret = session.execute(
        select([func.min(Result.rank)])
        .where(and_(
            Result.query_id == query.id,
            Result.version == query.version
        ))
    ).scalar()
    return 0 if ret is None else ret


def check_range(begin, end):
    if end is not None:
        assert_less_equal(begin, end)


def art_count_in_db(session):
    return session.query(Art).count()


def remote_no_change_at(query, i, session):
    art_in_db = head(get_arts_from_db(
        query_id=query.id,
        offset=i,
        limit=1,
        session=session
    ))
    if art_in_db is None:
        return False
    art_in_remote = head(get_arts_from_remote(query.text, begin=i))
    if art_in_remote is None:
        return False
    return same(art_in_db, art_in_remote)


def remote_no_change(query, begin, end, session):
    check_range(begin, end)
    if begin == end:
        return True
    first_in_db = head(get_arts_from_db(
        query_id=query.id,
        offset=begin,
        limit=1,
        session=session
    ))
    if first_in_db is None:
        return False
    if end is None:
        end = art_count_in_db(session)
    last_in_db = head(get_arts_from_db(
        query_id=query.id,
        offset=end - 1,
        limit=1,
        session=session
    ))
    if last_in_db is None:
        if query.total >= end:
            return False
        arts_in_remote = list(take(
            end - begin,
            get_arts_from_remote(query.text, begin=begin)
        ))
        if begin + len(arts_in_remote) == end:
            return False
        last_in_db = head(get_arts_from_db(
            query_id=query.id,
            offset=begin + len(arts_in_remote) - 1,
            limit=1,
            session=session
        ))
    else:
        arts_in_remote = []
    first_in_remote = head(get_arts_from_remote(query.text, begin=begin))
    if first_in_remote is None:
        return False
    if arts_in_remote:
        last_in_remote = arts_in_remote[-1]
    else:
        last_in_remote = head(get_arts_from_remote(query.text, begin=end - 1))
    if last_in_remote is None:
        return False
    return same(first_in_db, first_in_remote) and same(last_in_db, last_in_remote)


def same(lhs, rhs):
    return lhs.toraid == rhs.toraid and lhs.hash == rhs.hash


def get_arts_from_db(query_id, session, **kargs):
    idq = (
        select([Result.art_id.label('id'), Result.version, Result.rank])
        .where(Result.query_id == query_id)
        .order_by(desc(Result.version), Result.rank)
    )
    if 'offset' in kargs:
        idq = idq.offset(kargs['offset'])
    if 'limit' in kargs:
        idq = idq.limit(kargs['limit'])
    idq = idq.alias()
    return list(
        session.query(Art)
        .join(idq, Art.id == idq.c.id)
        .order_by(desc(idq.c.version), idq.c.rank)
        .all()
    )
