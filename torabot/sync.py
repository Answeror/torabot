'''
model used to sync tora and local database
'''


from .model import Art, Change, Query, Result
from .spider import list_all
from sqlalchemy.sql import exists, and_
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
        timestamp=d['timestamp'],
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


def ischanged(art, session):
    return not bool(session.query(exists().where(and_(
        Art.toraid == art.toraid,
        Art.timestamp == art.timestamp
    ))).scalar())


def add_art(art, session):
    session.add(art)


def has_art(art, session):
    return bool(session.query(exists().where(Art.toraid == art.toraid)).scalar())


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
    return bool(session.query(exists().where(Query.text == query.text)).scalar())


def put_new_query(query, session):
    if has_query(query=query, session=session):
        return session.query(Query).filter_by(text=query.text).one()
    session.add(query)
    return query


def add_result(query, art, rank, session):
    query.result.append(Result(query=query, art=art, rank=rank))


def sync(query, session):
    log.debug('sync start: {}', query)

    if has_query(text=query, session=session):
        query = session.query(Query).filter_by(text=query).one()
    else:
        query = Query(text=query)
        session.add(query)
        session.flush()
        session.refresh(query, ['id'])

    arts = []
    for art in map(dict_to_art, list_all(query.text)):
        isreserve, isnew = checkstate(art, session)
        if isreserve:
            add_reserve_change(art, session)
        if isnew:
            add_new_change(art, session)
            session.add(art)
        else:
            if ischanged(art, session):
                art = update_art(art, session)
            else:
                log.debug('{} unchange', art.toraid)
                break
        arts.append(art)

    session.flush()
    session.expire_all()

    art_ids = [art.id for art in arts]
    for id in (
        session.query(Result.art_id)
        .filter(Result.query_id == query.id)
        .all()
    ):
        if id not in (art.id for art in arts):
            art_ids.append(id)

    session.execute(
        Result.__table__
        .delete()
        .where(Result.query_id == query.id)
    )
    session.execute(
        Result.__table__
        .insert()
        .values(query_id=query.id),
        [{'art_id': id, 'rank': i} for i, id in enumerate(art_ids)]
    )
    session.flush()
    session.expire_all()

    log.debug('sync done, got {} arts', len(arts))
    return query.arts
