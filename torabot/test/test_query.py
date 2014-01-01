from .mixin import ModelMixin
from ..model import Session
from nose.tools import assert_equal, assert_is_not_none, assert_less
from .mock import mockrequests
from httmock import HTTMock
from ..query import query
from unittest.mock import patch, Mock
from ..time import tokyo_to_utc
from datetime import datetime
from contextlib import contextmanager
from .. import spider


@contextmanager
def gotopast(year):
    with patch('torabot.time._utcnow') as now:
        now.return_value = tokyo_to_utc(datetime(year=year, month=1, day=1))
        yield now
        now.assert_called_with()


def wrap_list_one_safe():
    return patch(
        'torabot.spider.list_one_safe',
        Mock(wraps=spider.list_one_safe)
    )


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

    def test_paged_query(self):
        s = Session()
        with gotopast(year=2010):
            with HTTMock(mockrequests):
                with wrap_list_one_safe() as mf:
                    a_20_30 = query('艦', begin=20, end=30, session=s)
                    assert_less(mf.call_count, 3)
                with wrap_list_one_safe() as mf:
                    a_15_30 = query('艦', begin=15, end=30, session=s)
                    assert_less(mf.call_count, 3)
                assert_equal(len(a_20_30), 10)
                assert_equal(len(a_15_30), 15)
                assert_equal(
                    [art.toraid for art in a_15_30[5:10]],
                    [art.toraid for art in a_20_30[:5]]
                )

    def test_paged_query_twice(self):
        s = Session()
        with gotopast(year=2010):
            with HTTMock(mockrequests):
                a_20_30 = query('艦', begin=20, end=30, session=s)
                a_15_30 = query('艦', begin=15, end=30, session=s)
                s.commit()
                a_20_30 = query('艦', begin=20, end=30, session=s)
                a_15_30 = query('艦', begin=15, end=30, session=s)
                assert_equal(len(a_20_30), 10)
                assert_equal(len(a_15_30), 15)
                assert_equal(
                    [art.toraid for art in a_15_30[5:10]],
                    [art.toraid for art in a_20_30[:5]]
                )

    def test_paged_query_futher(self):
        s = Session()
        with gotopast(year=2010):
            with HTTMock(mockrequests):
                a_10_20 = query('艦', begin=10, end=20, session=s)
                a_20_30 = query('艦', begin=20, end=30, session=s)
                assert_equal(len(a_20_30), 10)
