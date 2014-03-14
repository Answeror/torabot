from ..ut.session import makesession
from ..core.sync import strict
from ..core.const import SYNC_LIMIT
from ..spider.tora import FrozenSpider
from ..db import get_sorted_queries
from concurrent.futures import ThreadPoolExecutor as Ex


def make_engine(config):
    from sqlalchemy import create_engine
    return create_engine(config['TORABOT_CONNECTION_STRING'])


def sync_all(config):
    engine = make_engine(config)

    with makesession(engine=engine) as session:
        queries = get_sorted_queries(session.connection())

    with Ex(max_workers=config.get('TORABOT_SYNC_THREADS', 32)) as ex:
        for query in queries:
            ex.submit(_sync_one, query.text, engine)


def _sync_one(query, engine):
    spider = FrozenSpider()
    with makesession(engine=engine, commit=True) as session:
        strict(query, SYNC_LIMIT, spider, session.connection())
