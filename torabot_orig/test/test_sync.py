from nose.tools import assert_equal, assert_is_not_none
from .mixin import ModelMixin
from ..model import Session, Art, Change, Query
from ..sync import sync
from ..redis import redis
from .spider import UsotukiyaSpider as Spider


class TestSync(ModelMixin):

    def sync(self, session):
        sync('大嘘', 32, Spider(), session)

    def test_sync_broadcast(self):
        s = Session()
        self.sync(s)
        s.commit()
        assert_is_not_none(redis.lpop('change'))

    def test_sync(self):
        s = Session()
        self.sync(s)
        s.commit()
        assert_equal(s.query(Art).count(), 8)
        assert_equal(s.query(Change).filter(Change.what == Change.NEW).count(), 8)
        assert_equal(s.query(Query).count(), 1)

    def test_sync_twice(self):
        s = Session()
        self.sync(s)
        self.sync(s)
        s.commit()
        assert_equal(s.query(Art).count(), 8)
        assert_equal(s.query(Change).filter(Change.what == Change.NEW).count(), 8)
        assert_equal(s.query(Query).count(), 1)
