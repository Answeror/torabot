from concurrent.futures import ThreadPoolExecutor as Ex
from ..ut.guard import exguard, timeguard
from ..core.connection import autoccontext
from ..core.sync import sync, fast_sync
from ..core.backends.postgresql import PostgreSQL
from ..core.query import regular
from ..db import get_need_sync_queries
from .engine import make as make_engine
from logbook import Logger


log = Logger(__name__)


def _sync(engine, func, kind, text, timeout):
    with autoccontext(engine=engine, commit=True) as conn:
        func(
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

    options = dict(
        engine=engine,
        timeout=conf['TORABOT_SPY_TIMEOUT'],
    )

    with Ex(max_workers=conf['TORABOT_SYNC_THREADS']) as ex:
        for kind, text in unique(queries):
            # log.debug('sync {} of {}', text, kind)
            ex.submit(
                exguard(_sync),
                func=sync,
                kind=kind,
                text=text,
                **options
            )

    with Ex(max_workers=conf['TORABOT_SYNC_THREADS']) as ex:
        for query in queries:
            ex.submit(
                exguard(_sync),
                func=fast_sync,
                kind=query.kind,
                text=query.text,
                **options
            )


def unique(queries):
    result = {regular(q.kind, q.text) for q in queries}
    log.info('reduce {} queries to {} regular ones', len(queries), len(result))
    return result
