from .g import g
from .mixin import ModelMixin
from ..model import Session, Art
from nose.tools import assert_equal
from .mock import mockrequests
from httmock import HTTMock
from ..sync import sync


class TestSync(ModelMixin):

    def setup(self):
        self.transaction = g.connection.begin()

    def teardown(self):
        self.transaction.rollback()

    def test_add_art(self):
        s = Session()
        with HTTMock(mockrequests):
            sync('大嘘', s)
        assert_equal(s.query(Art).count(), 8)
