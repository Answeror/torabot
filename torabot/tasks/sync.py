from concurrent.futures import ThreadPoolExecutor as Ex
from ..ut.guard import exguard, timeguard
from ..core.connection import autoccontext
from ..core.sync import sync
from ..core.backends.postgresql import PostgreSQL
from ..db import get_need_sync_queries
from .engine import make as make_engine
from logbook import Logger


log = Logger(__name__)


def _sync(engine, kind, text, timeout):
    with autoccontext(engine=engine) as conn:
        sync(
            kind=kind,
            text=text,
            timeout=timeout,
            backend=PostgreSQL(conn=conn)
        )


@timeguard
def sync_all(conf):
    engine = make_engine(conf)

    with autoccontext(engine=engine) as conn:
        queries = get_need_sync_queries(conn)

    with Ex(max_workers=conf['TORABOT_SYNC_THREADS']) as ex:
        for query in queries:
            log.debug('sync {} of {}', query.text, query.kind)
            ex.submit(
                exguard(_sync),
                engine=engine,
                kind=query.kind,
                text=query.text,
                timeout=conf['TORABOT_SPY_TIMEOUT'],
            )
