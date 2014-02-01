from nose.tools import assert_equal
from httmock import HTTMock
from datetime import datetime
from .mock import mockrequests
from .const import USOTUKIYA
from ..time import tokyo_to_utc
from ..spider import gen_arts, ptime


def test_gen_arts():
    with HTTMock(mockrequests):
        arts = list(gen_arts('大嘘'))
    assert_equal(arts, USOTUKIYA)


def test_tokyo_to_utc():
    with HTTMock(mockrequests):
        assert_equal(
            ptime('http://www.toranoana.jp/mailorder/article/04/0030/16/24/040030162479.html'),
            tokyo_to_utc(datetime(year=2013, month=12, day=31))
        )
