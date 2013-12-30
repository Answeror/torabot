from .sync import sync, has_query
from .model import Query
from sqlalchemy.orm import joinedload
from logbook import Logger
from .spider import long_fetch_ptime
from nose.tools import assert_is_not_none
import requests


log = Logger(__name__)


class Art(object):

    def __init__(self, base, dbsession, netsession):
        self.base = base
        self.dbsession = dbsession
        self.netsession = netsession

    def __getattr__(self, key):
        return getattr(self.base, key)

    @property
    def ptime(self):
        if self.base.ptime is None:
            self.base.ptime = long_fetch_ptime(self.uri, self.netsession)
            self.base = self.dbsession.merge(self.base)
        assert_is_not_none(self.base.ptime)
        return self.base.ptime


def makearts(arts, dbsession):
    netsession = requests.Session()
    for art in arts:
        yield Art(art, dbsession=dbsession, netsession=netsession)


def query(text, session):
    log.debug('query: {}', text)
    if not has_query(text=text, session=session):
        return list(makearts(sync(text, session=session), session))
    log.debug('already synced, pull from database')
    return list(makearts((
        session.query(Query)
        .filter_by(text=text)
        .options(joinedload(Query.result))
        .one()
    ).arts, session))
