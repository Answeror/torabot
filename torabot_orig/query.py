from .sync import sync, has_query, arts_from_db
from .model import Query
from logbook import Logger
from nose.tools import assert_less_equal


SYNC_LIMIT = 32


log = Logger(__name__)


def from_remote(begin, end, session, spider, return_query=False, **kargs):
    if 'query_text' in kargs:
        text = kargs['query_text']
    elif 'query' in kargs:
        text = kargs['query'].text
    else:
        assert False, 'neither query_text nor query provided'
    sync(
        text,
        n=SYNC_LIMIT if end is None else end,
        spider=spider,
        session=session,
    )
    session.flush()
    if 'query' in kargs:
        query = kargs['query']
    else:
        assert has_query(text=text, session=session)
        query = get_query(text, session)
    arts = arts_from_db(
        query.id,
        offset=begin,
        session=session,
        **({} if end is None else {'limit': end - begin})
    )
    return arts if not return_query else (arts, query)


def get_query(text, session):
    return session.query(Query).filter_by(text=text).one()


def check_range(begin, end):
    if end is not None:
        assert_less_equal(begin, end)


def query(text, spider, session, begin=0, end=None, return_detail=False):
    check_range(begin, end)

    log.debug('query {} in ({}, {})', text, begin, end)
    if not has_query(text=text, session=session):
        arts, query = from_remote(
            query_text=text,
            begin=begin,
            end=end,
            return_query=True,
            spider=spider,
            session=session
        )
    else:
        log.debug('{} already synced, pull from database')
        query = get_query(text, session)
        arts = from_db_and_remote(query, begin, end, spider, session)

    return arts if not return_detail else {
        'arts': arts,
        'total': query.total
    }


def not_enough(begin, end, arts):
    return end is None or begin + len(arts) < end


def has_more(begin, query, arts):
    return begin + len(arts) < query.total


def from_db_and_remote(query, begin, end, spider, session):
    arts = arts_from_db(
        query_id=query.id,
        offset=begin,
        session=session,
        **({} if end is None else {'limit': end - begin})
    )
    if not_enough(begin, end, arts) and has_more(begin, query, arts):
        return from_remote(
            query=query,
            begin=begin,
            end=end,
            spider=spider,
            session=session,
        )
    return arts
