'''
model used to sync tora and local database
'''


from .model import Art, Change, Query, Result
from .spider import list_all
from sqlalchemy.sql import exists, and_, func, update, select
from . import state
from . import what
from logbook import Logger


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


def add_art(art, session):
    session.add(art)


def has_art(art, session):
    return bool(session.query(
        exists()
        .where(Art.toraid == art.toraid)
    ).scalar())


def update_art(art, session):
    art.id = session.query(Art).filter_by(toraid=art.toraid).one().id
    return session.merge(art)


def add_reserve_change(art, session):
    session.add(Change(art=art, what=what.RESERVE))


def add_new_change(art, session):
    session.add(Change(art=art, what=what.NEW))


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
        return query
    query = Query(text=text)
    session.add(query)
    session.flush()
    session.expire(query, ['id'])
    return query


def update_arts(query, limit, session):
    for turn, art in zip(
        range(limit + 1),
        map(dict_to_art, list_all(query.text))
    ):
        if turn == limit:
            log.info('sync limit({}) reached for query {}', limit, query.text)
            break

        isreserve, isnew = checkstate(art, session)
        if isreserve:
            add_reserve_change(art, session)
        if isnew:
            add_new_change(art, session)
            session.add(art)
            session.flush()
            session.expire(art, ['id'])
        else:
            if art_changed(art, session):
                art = update_art(art, session)
            if query_result_changed(query.id, art, session):
                update_query_result(query, art, session)
            else:
                log.debug('{} unchange', art.toraid)
                break
        yield art


def update_query_result(query, art, session):
    session.execute(
        update(Result)
        .where(and_(
            Result.query_id == query.id,
            Result.art_id == art.id
        ))
        .values(
            version=query.version,
            hash=art.hash,
            rank=(
                select([func.max(Result.rank) + 1])
                .where(and_(
                    Result.query_id == query.id,
                    Result.version == query.version
                ))
                .correlate()
                .as_scalar()
            )
        )
    )


def refresh(session):
    session.flush()
    session.expire_all()


def sync(query, session, limit=1024):
    return list(gensync(query, session, limit))


def gensync(query, session, limit=1024):
    log.debug('sync start: {}', query)

    query = put_query(query, session)
    count = 0
    for art in update_arts(query, limit, session):
        yield art
        count += 1

    log.debug('sync done, update {} arts', count)
