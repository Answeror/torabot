from .sync import sync, has_query
from .model import Query, Result, Art
from sqlalchemy.sql import select, desc
from logbook import Logger
from fn.iters import drop, take


log = Logger(__name__)


def query(text, session, **kargs):
    log.debug('query {} with options {}', text, kargs)

    page = kargs.get('page')
    room = kargs.get('room')

    if not has_query(text=text, session=session):
        gen = lambda: sync(text, session=session)
        if page is None or room is None:
            arts = list(gen())
        else:
            arts = list(take(room, drop(page * room, gen())))
        if room is None or len(arts) < room:
            assert has_query(text=text, session=session)
            if page is None or room is None:
                rest = _query(
                    text=text,
                    offset=len(arts),
                    session=session
                )
            else:
                rest = _query(
                    text=text,
                    offset=page * room + len(arts),
                    limit=room - len(arts),
                    session=session
                )
            return arts + rest

    log.debug('already synced, pull from database')

    if page is None or room is None:
        return _query(text=text, session=session)

    return _query(
        text=text,
        offset=page * room,
        limit=room,
        session=session
    )


def _query(text, session, **kargs):
    idq = (
        select([Result.art_id.label('id'), Result.rank])
        .where(Result.query_id == (
            select([Query.id])
            .where(Query.text == text)
            .alias()
        ).c.id)
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
        .order_by(idq.c.rank)
        .all()
    )
