from .mixin import ModelMixin
from ..model import Session, User
from .mock import mockrequests
from httmock import HTTMock
from ..sub import sub, unsub, has_sub
from ..sync import sync


class TestSub(ModelMixin):

    def prepare(self, s):
        with HTTMock(mockrequests):
            sync('大嘘', s)
        user = User(name='foo', email='bar', openid='http://foobar.com')
        s.add(user)
        s.flush()
        s.expire(user, ['id'])
        self.user_id = user.id

    def test_sub(self):
        s = Session()
        self.prepare(s)
        sub(user_id=self.user_id, query_text='大嘘', session=s)
        s.commit()
        assert has_sub(user_id=self.user_id, query_text='大嘘', session=s)

    def test_sub_twice(self):
        s = Session()
        self.prepare(s)
        sub(user_id=self.user_id, query_text='大嘘', session=s)
        s.commit()
        assert has_sub(user_id=self.user_id, query_text='大嘘', session=s)
        # must use savepoint here
        # otherwise outer transaction will rollback
        # http://stackoverflow.com/a/13438234/238472
        s.begin_nested()
        sub(user_id=self.user_id, query_text='大嘘', session=s)
        s.commit()
        assert has_sub(user_id=self.user_id, query_text='大嘘', session=s)

    def test_unsub(self):
        s = Session()
        self.prepare(s)
        sub(user_id=self.user_id, query_text='大嘘', session=s)
        s.commit()
        unsub(user_id=self.user_id, query_text='大嘘', session=s)
        s.commit()
        assert not has_sub(user_id=self.user_id, query_text='大嘘', session=s)

    def test_unsub_twice(self):
        s = Session()
        self.prepare(s)
        sub(user_id=self.user_id, query_text='大嘘', session=s)
        s.commit()
        unsub(user_id=self.user_id, query_text='大嘘', session=s)
        s.commit()
        assert not has_sub(user_id=self.user_id, query_text='大嘘', session=s)
        unsub(user_id=self.user_id, query_text='大嘘', session=s)
        s.commit()
        assert not has_sub(user_id=self.user_id, query_text='大嘘', session=s)
