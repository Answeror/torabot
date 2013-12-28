'''
model used to sync tora and local database
'''


from .model import Art
from .spider import fetch_and_parse_all
from sqlalchemy.sql import exists, and_
from . import state


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
    return bool(session.query(exists().where(
        Art.toraid == art.toraid
    )).scalar())


def isreserve(art, session):
    return bool(session.query(exists().where(and_(
        Art.toraid == art.toraid,
        Art.state == state.RESERVE
    ))).scalar())


def add_art(art, session):
    session.add(art)


def put_art(art, session):
    session.merge(art)


def add_reserve_notification(art, session):
    pass


def add_new_notification(art, session):
    pass


def sync(query, session):
    for art in map(art_from_dict, fetch_and_parse_all(query)):
        if isreserve(art, session):
            add_reserve_notification(art, session)
        if isnew(art, session):
            add_new_notification(art, session)
            add_art(art, session)
        else:
            put_art(art, session)
