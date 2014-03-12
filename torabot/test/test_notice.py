from .mixin import ModelMixin
from ..model import Session, User, Query, Result, Art, Change
from .mock import mockrequests
from httmock import HTTMock
from ..sync import sync
from ..notice import pop_change, pop_changes, listen, pop_notices, Notice
from ..sub import sub
from nose.tools import assert_equal, assert_is_none, assert_is_not_none
from ..redis import redis
from ..spider import FrozenSpider as Spider


class TestNotice(ModelMixin):

    def setup(self):
        ModelMixin.setup(self)
        redis.delete('notice')
        self.spider = Spider()
        self.session = Session()

    def teardown(self):
        self.session.close()
        redis.delete('notice')
        ModelMixin.teardown(self)

    def sync(self, spider=None, session=None):
        if spider is None:
            spider = self.spider
        if session is None:
            session = self.session
        with HTTMock(mockrequests):
            sync('大嘘', n=32, spider=spider, session=session)
        self.session.commit()

    def prepare(self, session=None):
        if session is None:
            session = self.session
        self.user = User(name='foo', email='bar', openid='http://foobar.com')
        session.add(self.user)
        session.commit()
        session.expire_all()
        if session.query(Query).filter_by(text='大嘘').first() is None:
            session.add(Query(text='大嘘'))
            session.commit()
        sub(user_id=self.user.id, query_text='大嘘', session=session)
        session.commit()

    def test_pop_change(self):
        self.sync()
        new_count = 0
        for i in range(8):
            change = pop_change(self.session)
            assert change is not None
            if change.what == Change.NEW:
                new_count += 1
            else:
                assert False
        assert_is_none(pop_change(self.session))
        assert_equal(new_count, 8)

    def test_notice(self):
        self.prepare()
        self.sync()
        pop_changes(self.session)
        assert_equal(len(self.user.notices), 8)

    def test_notice_reserve(self):
        self.prepare()
        self.sync()
        pop_changes(self.session)
        self.session.commit()
        assert_equal(len(self.user.notices), 8)
        first_art = (
            self.session.query(Result)
            .join(Query)
            .filter(Query.text == '大嘘')
            .filter(Result.rank == 0)
            .one()
        ).art
        first_art.state = Art.OTHER
        first_art.hash = ''
        self.session.commit()
        self.sync()
        pop_changes(self.session)
        self.session.commit()
        assert_equal(len(self.user.notices), 9)

    def test_notice_redis(self):
        self.prepare()
        self.sync()
        pop_changes(self.session)
        self.session.commit()
        assert_is_not_none(redis.lpop('notice'))

    def test_listen(self):
        self.prepare()
        self.sync()
        listen('change', lambda: pop_changes(self.session))
        assert_equal(len(self.user.notices), 8)

    def test_pop_notices(self):
        self.prepare()
        self.sync()
        pop_changes(self.session)

        self.count = 0

        def eat(notice, session):
            self.count += 1
            return self.count <= 7

        pop_notices(eat, self.session)
        self.session.commit()
        assert_equal((
            self.session.query(Notice)
            .filter_by(state=Notice.PENDING)
            .count()
        ), 1)
        assert_equal((
            self.session.query(Notice)
            .filter_by(state=Notice.EATEN)
            .count()
        ), 7)
