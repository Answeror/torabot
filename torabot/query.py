from .sync import sync, has_query
from .model import Query, Result, Art
from sqlalchemy.sql import select, desc
from logbook import Logger
from nose.tools import assert_less_equal


log = Logger(__name__)


def from_remote(begin, end, session, **kargs):
    if 'query_text' in kargs:
        text = kargs['query_text']
    elif 'query' in kargs:
        text = kargs['query'].text
    else:
        assert False, 'neither query_text nor query provided'
    sync(
        text,
        session=session,
        begin=begin,
        **({} if end is None else {'end': end})
    )
    session.flush()
    if 'query' in kargs:
        query = kargs['query']
    else:
        assert has_query(text=text, session=session)
        query = get_query(text, session)
    return _query(
        query.id,
        offset=begin,
        session=session,
        **({} if end is None else {'limit': end - begin})
    )


def get_query(text, session):
    return session.query(Query).filter_by(text=text).one()


def query(text, session, begin=0, end=None, return_detail=False):
    log.debug('query {} in ({}, {})', text, begin, end)

    if end is not None:
        assert_less_equal(begin, end)
    if not has_query(text=text, session=session):
        return from_remote(
            query_text=text,
            begin=begin,
            end=end,
            session=session
        )
    query = get_query(text, session)

    log.debug('already synced, pull from database')
    arts = from_db(query, begin, end, session)
    return arts if not return_detail else {
        'arts': arts,
        'total': query.total
    }


def from_db(query, begin, end, session):
    arts = _query(
        query.id,
        offset=begin,
        session=session,
        **({} if end is None else {'limit': end - begin})
    )
    if end is None or begin + len(arts) < end:
        if begin + len(arts) < query.total:
            return from_remote(
                query=query,
                begin=begin,
                end=end,
                session=session
            )
    return arts


def _query(query_id, session, **kargs):
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
