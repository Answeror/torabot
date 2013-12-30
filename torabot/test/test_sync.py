from .g import g
from .mixin import ModelMixin
from ..model import Session, Art, Change, Query
from nose.tools import assert_equal
from .mock import mockrequests
from httmock import HTTMock
from ..sync import sync
from .. import what
from mock import patch
from ..time import tokyo_to_utc
from datetime import datetime


class TestSync(ModelMixin):

    def sync(self, session):
        with patch('torabot.spider.utcnow') as now:
            now.return_value = tokyo_to_utc(datetime(year=2010, month=1, day=1))
            with HTTMock(mockrequests):
                sync('大嘘', session)
            now.assert_called_with()
        session.flush()

    def test_sync(self):
        s = Session()
        self.sync(s)
        assert_equal(s.query(Art).count(), 8)
        assert_equal(s.query(Change).filter(Change.what == what.NEW).count(), 8)
        assert_equal(s.query(Change).filter(Change.what == what.RESERVE).count(), 2)
        assert_equal(s.query(Query).count(), 1)
        assert_equal(len(list(s.query(Query).one().arts)), 8)

    def test_sync_twice(self):
        s = Session()
        self.sync(s)
        self.sync(s)
        assert_equal(s.query(Art).count(), 8)
        assert_equal(s.query(Change).filter(Change.what == what.NEW).count(), 8)
        assert_equal(s.query(Change).filter(Change.what == what.RESERVE).count(), 2)
        assert_equal(s.query(Query).count(), 1)
        assert_equal(len(list(s.query(Query).one().arts)), 8)
