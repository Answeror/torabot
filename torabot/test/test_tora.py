from nose.tools import assert_equal
from ..tora import order_uri_from_toraid, toraid_from_order_uri


URI = 'http://www.toranoana.jp/mailorder/article/04/0030/17/39/040030173983.html'
ID = '040030173983'


def test_order_uri_from_toraid():
    assert_equal(order_uri_from_toraid(ID), URI)


def test_toraid_from_order_uri():
    assert_equal(toraid_from_order_uri(URI), ID)
