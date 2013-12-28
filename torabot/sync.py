'''
model used to sync tora and local database
'''


from .model import Art, Change
from .spider import fetch_and_parse_all
from sqlalchemy.sql import exists, and_
from . import state
from . import what


def art_from_dict(d):
    art = Art(
        title=d['title'],
        author=d['author'],
        comp=d['comp'],
        state=state.RESERVE if d['reserve'] else state.OTHER,
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


def add_art(art, session):
    session.add(art)


def put_art(art, session):
    session.merge(art)


def add_reserve_change(art, session):
    session.add(Change(art=art, what=what.RESERVE))


def add_new_change(art, session):
    session.add(Change(art=art, what=what.NEW))


def checkstate(art, session):
    return (
        isreserve(art, session),
        isnew(art, session),
    )


def sync(query, session):
    session.flush()
    for art in map(art_from_dict, fetch_and_parse_all(query)):
        isreserve, isnew = checkstate(art, session)
        if isreserve:
            add_reserve_change(art, session)
            session.flush()
        if isnew:
            add_new_change(art, session)
            add_art(art, session)
            session.flush()
        else:
            put_art(art, session)
            session.flush()
