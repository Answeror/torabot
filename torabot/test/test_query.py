from .mixin import ModelMixin
from ..model import Session
from nose.tools import assert_equal
from .mock import mockrequests
from httmock import HTTMock
from ..query import query


class TestSync(ModelMixin):

    def test_query(self):
        s = Session()
        with HTTMock(mockrequests):
            assert_equal(len(query('大嘘', s)), 8)
