from .mixin import ModelMixin
from ..model import Session
from nose.tools import assert_equal, assert_is_not_none
from .mock import mockrequests
from httmock import HTTMock
from ..query import query
from mock import patch
from ..time import tokyo_to_utc
from datetime import datetime
from contextlib import contextmanager


@contextmanager
def gotopast(year):
    with patch('torabot.time._utcnow') as now:
        now.return_value = tokyo_to_utc(datetime(year=year, month=1, day=1))
        yield now
        now.assert_called_with()


class TestQuery(ModelMixin):

    def test_query(self):
        s = Session()
        with gotopast(year=2010):
            with HTTMock(mockrequests):
                assert_equal(len(query('大嘘', s)), 8)

    def test_ptime(self):
        s = Session()
        with gotopast(year=2010):
            with HTTMock(mockrequests):
                for art in query('大嘘', s):
                    assert_is_not_none(art.ptime)

    def test_query_less(self):
        s = Session()
        with gotopast(year=2014):
            with HTTMock(mockrequests):
                assert_equal(len(query('大嘘', s)), 0)
