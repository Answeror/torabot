from .sync import sync, has_query
from .model import Query
from sqlalchemy.orm import joinedload
from logbook import Logger


log = Logger(__name__)


def query(text, session):
    log.debug('query: {}', text)
    if not has_query(text=text, session=session):
        return list(sync(text, session=session))
    log.debug('already synced, pull from database')
    return list((
        session.query(Query)
        .filter_by(text=text)
        .options(joinedload(Query.result))
        .one()
    ).arts)
