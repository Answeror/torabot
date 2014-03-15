from concurrent.futures import ThreadPoolExecutor as Ex
from ..ut.connection import ccontext
from ..core.sync import strict
from ..spider.tora import FrozenSpider
from ..db import get_sorted_queries
from .engine import make as make_engine


def sync_all(conf):
    engine = make_engine(conf)

    with ccontext(engine=engine) as conn:
        queries = get_sorted_queries(conn)

    with Ex(max_workers=conf['TORABOT_SYNC_THREADS']) as ex:
        for query in queries:
            ex.submit(
                _sync_one,
                conf['TORABOT_PAGE_ROOM'],
                query.text,
                engine,
            )


def sync_one(query, conf):
    engine = make_engine(conf)
    _sync_one(conf['TORABOT_PAGE_ROOM'], query, engine)


def _sync_one(n, query, engine):
    with ccontext(commit=True, engine=engine) as conn:
        strict(
            query,
            n,
            spider=FrozenSpider(),
            conn=conn,
        )
