from .g import g
from .mixin import ModelMixin
from ..model import Session, Art, Change
from nose.tools import assert_equal
from .mock import mockrequests
from httmock import HTTMock
from ..sync import sync
from .. import what


class TestSync(ModelMixin):

    def test_add_art(self):
        s = Session()
        with HTTMock(mockrequests):
            sync('大嘘', s)
        s.commit()
        assert_equal(s.query(Art).count(), 8)
        assert_equal(s.query(Change).filter(Change.what == what.NEW).count(), 8)
        assert_equal(s.query(Change).filter(Change.what == what.RESERVE).count(), 2)
