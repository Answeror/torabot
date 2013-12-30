from .mixin import ModelMixin
from ..model import Session
from nose.tools import assert_equal
from .mock import mockrequests
from httmock import HTTMock
from ..query import query
from mock import patch
from ..time import tokyo_to_utc
from datetime import datetime


class TestQuery(ModelMixin):

    def test_query(self):
        s = Session()
        with patch('torabot.spider.utcnow') as now:
            now.return_value = tokyo_to_utc(datetime(year=2010, month=1, day=1))
            with HTTMock(mockrequests):
                assert_equal(len(query('大嘘', s)), 8)
            now.assert_called_with()
