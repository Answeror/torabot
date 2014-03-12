from httmock import HTTMock
from ..sub import sub, unsub, has_sub
from ..sync import sync
from ..spider import FrozenSpider as Spider
from ..model import Session, User
from .mixin import ModelMixin
from .mock import mockrequests


class TestSub(ModelMixin):

    def setup(self):
        ModelMixin.setup(self)
        self.spider = Spider()
        self.session = Session()

    def teardown(self):
        self.session.close()
        ModelMixin.teardown(self)

    def prepare(self, spider=None, session=None):
        if spider is None:
            spider = self.spider
        if session is None:
            session = self.session
        with HTTMock(mockrequests):
            sync('大嘘', n=32, spider=spider, session=session)
        user = User(name='foo', email='bar', openid='http://foobar.com')
        session.add(user)
        session.commit()
        self.user_id = user.id

    def test_sub(self):
        self.prepare()
        sub(user_id=self.user_id, query_text='大嘘', session=self.session)
        self.session.commit()
        assert has_sub(user_id=self.user_id, query_text='大嘘', session=self.session)

    def test_sub_twice(self):
        self.prepare()
        sub(user_id=self.user_id, query_text='大嘘', session=self.session)
        self.session.commit()
        assert has_sub(user_id=self.user_id, query_text='大嘘', session=self.session)
        # must use savepoint here
        # otherwise outer transaction will rollback
        # http://stackoverflow.com/a/13438234/238472
        self.session.begin_nested()
        sub(user_id=self.user_id, query_text='大嘘', session=self.session)
        self.session.commit()
        assert has_sub(user_id=self.user_id, query_text='大嘘', session=self.session)

    def test_unsub(self):
        self.prepare()
        sub(user_id=self.user_id, query_text='大嘘', session=self.session)
        self.session.commit()
        unsub(user_id=self.user_id, query_text='大嘘', session=self.session)
        self.session.commit()
        assert not has_sub(user_id=self.user_id, query_text='大嘘', session=self.session)

    def test_unsub_twice(self):
        self.prepare()
        sub(user_id=self.user_id, query_text='大嘘', session=self.session)
        self.session.commit()
        unsub(user_id=self.user_id, query_text='大嘘', session=self.session)
        self.session.commit()
        assert not has_sub(user_id=self.user_id, query_text='大嘘', session=self.session)
        unsub(user_id=self.user_id, query_text='大嘘', session=self.session)
        self.session.commit()
        assert not has_sub(user_id=self.user_id, query_text='大嘘', session=self.session)
