from concurrent.futures import ThreadPoolExecutor as Ex
from ..ut.session import makesession
from ..core.sync import strict
from ..core.const import SYNC_LIMIT
from ..spider.tora import FrozenSpider
from ..db import get_sorted_queries
from .engine import make as make_engine


def sync_all(conf):
    engine = make_engine(conf)

    with makesession(engine=engine) as session:
        queries = get_sorted_queries(session.connection())

    with Ex(max_workers=conf['TORABOT_SYNC_THREADS']) as ex:
        for query in queries:
            ex.submit(_sync_one, query.text, engine)


def _sync_one(query, engine):
    spider = FrozenSpider()
    with makesession(engine=engine, commit=True) as session:
        strict(query, SYNC_LIMIT, spider, session.connection())
