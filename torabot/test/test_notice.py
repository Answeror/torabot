from .mixin import ModelMixin
from ..model import Session
from .mock import mockrequests
from httmock import HTTMock
from ..sync import sync
from ..notice import pop_change
from .. import what
from nose.tools import assert_equal


class TestNotice(ModelMixin):

    def sync(self, session):
        with HTTMock(mockrequests):
            sync('大嘘', session)
        session.flush()

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
        assert pop_change(s) is None
        assert_equal(new_count, 8)
        assert_equal(reserve_count, 2)
