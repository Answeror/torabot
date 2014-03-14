from ..ut.session import makesession
from ..core.sync import strict
from ..core.const import SYNC_LIMIT
from ..spider.tora import FrozenSpider
from ..db import get_sorted_queries


def sync_all(config):
    spider = FrozenSpider()
    with makesession(config) as session:
        for query in get_sorted_queries(session.connection()):
            strict(query.text, SYNC_LIMIT, spider, session.connection())
            session.commit()
