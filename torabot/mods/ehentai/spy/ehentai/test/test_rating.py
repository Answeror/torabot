from nose.tools import assert_equal
from ..rating import parse_rating


def test_parse_rating():
    assert_equal(parse_rating('background-position:-16px -21px; opacity:1'), 3.5)
    assert_equal(parse_rating('background-position:-64px -21px; opacity:0.6'), 0.5)
    assert_equal(parse_rating('background-position:0px -1px; opacity:0.66666666666667'), 5)
