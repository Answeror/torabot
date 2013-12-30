from .sync import sync, has_query
from .model import Query
from sqlalchemy.orm import joinedload
from logbook import Logger
from .spider import long_fetch_ptime
import requests
from .time import utcnow
import concurrent.futures


log = Logger(__name__)


def makearts(arts):
    session = requests.Session()
    get = lambda art: art.ptime if art.ptime else long_fetch_ptime(art.uri, session)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for art, ptime in zip(arts, ex.map(get, arts)):
            art.ptime = ptime
            if art.ptime >= utcnow():
                yield art


def query(text, session):
    log.debug('query: {}', text)
    if not has_query(text=text, session=session):
        return list(makearts(sync(text, session=session)))
    log.debug('already synced, pull from database')
    return list(makearts((
        session.query(Query)
        .filter_by(text=text)
        .options(joinedload(Query.result))
        .one()
    ).arts))
