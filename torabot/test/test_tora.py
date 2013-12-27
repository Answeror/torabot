from nose.tools import assert_equal
from ..tora import order_uri_from_toraid


def test_order_uri_from_toraid():
    assert_equal(
        order_uri_from_toraid('040030173983'),
        'http://www.toranoana.jp/mailorder/article/04/0030/17/39/040030173983.html'
    )
