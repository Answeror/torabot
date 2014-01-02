from .mixin import ModelMixin
from ..model import Session, User, Query
from .mock import mockrequests
from httmock import HTTMock
from ..sync import sync, gensync
from ..notice import pop_change, pop_changes, listen
from .. import what
from ..sub import sub
from nose.tools import assert_equal, assert_is_none, assert_is_not_none
from ..redis import redis


class TestNotice(ModelMixin):

    def setup(self):
        ModelMixin.setup(self)
        redis.delete('notice')

    def teardown(self):
        redis.delete('notice')
        ModelMixin.teardown(self)

    def sync(self, session):
        with HTTMock(mockrequests):
            sync('大嘘', session=session)
        session.commit()

    def test_pop_change(self):
        s = Session()
        self.sync(s)
        new_count = 0
        reserve_count = 0
        for i in range(10):
            change = pop_change(s)
            assert change is not None
            if change.what == what.NEW:
                new_count += 1
            elif change.what == what.RESERVE:
                reserve_count += 1
            else:
                assert False
        assert_is_none(pop_change(s))
        assert_equal(new_count, 8)
        assert_equal(reserve_count, 2)

    def prepare(self, s):
        self.user = User(name='foo', email='bar', openid='http://foobar.com')
        s.add(self.user)
        s.flush()
        s.expire(self.user, ['id'])
        if s.query(Query).filter_by(text='大嘘').first() is None:
            s.add(Query(text='大嘘'))
            s.commit()
        sub(user_id=self.user.id, query_text='大嘘', session=s)
        s.commit()

    def test_notice(self):
        s = Session()
        self.prepare(s)
        self.sync(s)
        pop_changes(s)
        assert_equal(len(self.user.notices), 10)

    def test_notice_redis(self):
        s = Session()
        self.prepare(s)
        self.sync(s)
        pop_changes(s)
        s.commit()
        assert_is_not_none(redis.lpop('notice'))

    def test_notice_less(self):
        s = Session()
        with HTTMock(mockrequests):
            list(gensync('大嘘', begin=0, end=4, session=s))
        s.commit()
        self.prepare(s)
        pop_changes(s)
        s.commit()
        assert_equal(len(self.user.notices), 0)
        with HTTMock(mockrequests):
            list(gensync('大嘘', begin=4, session=s))
        s.commit()
        pop_changes(s)
        s.commit()
        assert_equal(len(self.user.notices), 4)

    def test_listen(self):
        s = Session()
        self.prepare(s)
        self.sync(s)
        s.commit()
        listen('change', lambda: pop_changes(s))
        assert_equal(len(self.user.notices), 10)
