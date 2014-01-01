from .mixin import ModelMixin
from ..model import Session, Art, Change, Query
from nose.tools import assert_equal
from .mock import mockrequests
from httmock import HTTMock
from ..sync import sync, min_rank
from ..what import NEW, RESERVE


class TestSync(ModelMixin):

    def sync(self, session):
        with HTTMock(mockrequests):
            sync('大嘘', session)

    def test_sync(self):
        s = Session()
        self.sync(s)
        assert_equal(s.query(Art).count(), 8)
        assert_equal(s.query(Change).filter(Change.what == NEW).count(), 8)
        assert_equal(s.query(Change).filter(Change.what == RESERVE).count(), 2)
        assert_equal(s.query(Query).count(), 1)

    def test_sync_twice(self):
        s = Session()
        self.sync(s)
        self.sync(s)
        assert_equal(s.query(Art).count(), 8)
        assert_equal(s.query(Change).filter(Change.what == NEW).count(), 8)
        assert_equal(s.query(Change).filter(Change.what == RESERVE).count(), 2)
        assert_equal(s.query(Query).count(), 1)

    def test_sync_limit(self):
        s = Session()
        with HTTMock(mockrequests):
            sync('大嘘', limit=4, session=s)
        assert_equal(s.query(Art).count(), 4)
        assert_equal(s.query(Change).filter(Change.what == NEW).count(), 4)
        assert_equal(s.query(Change).filter(Change.what == RESERVE).count(), 2)
        assert_equal(s.query(Query).count(), 1)

    def test_sync_begin_always_start_from_head(self):
        s = Session()
        with HTTMock(mockrequests):
            sync('大嘘', begin=3, session=s)
        q = s.query(Query).filter_by(text='大嘘').one()
        assert_equal(min_rank(q, s), 0)
        assert_equal(s.query(Art).count(), 8)
        assert_equal(s.query(Change).filter(Change.what == NEW).count(), 8)
        assert_equal(s.query(Change).filter(Change.what == RESERVE).count(), 2)
        assert_equal(s.query(Query).count(), 1)

    def test_min_rank_none(self):
        s = Session()
        q = Query(text='a')
        s.add(q)
        s.commit()
        assert_equal(min_rank(q, s), 0)
