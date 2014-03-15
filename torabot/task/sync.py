from ..ut.session import makesession
from ..core.sync import strict
from ..core.const import SYNC_LIMIT
from ..spider.tora import FrozenSpider
from ..db import get_sorted_queries
from .engine import make as make_engine


def sync_all(conf):
    from .. import celery

    engine = make_engine(conf)

    with makesession(engine=engine) as session:
        for query in get_sorted_queries(session.connection()):
            celery.sync_one.delay(query.text)


def sync_one(query, conf):
    engine = make_engine(conf)
    _sync_one(query, engine)


def _sync_one(query, engine):
    spider = FrozenSpider()
    with makesession(engine=engine, commit=True) as session:
        strict(query, SYNC_LIMIT, spider, session.connection())
