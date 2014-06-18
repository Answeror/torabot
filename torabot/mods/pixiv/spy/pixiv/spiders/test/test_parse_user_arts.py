import os
from nose.tools import assert_greater
from scrapy.selector import Selector
from .. import parse_user_arts


CURRENT_PATH = os.path.dirname(__file__)


def test_parse_user_arts():
    for name in [
        '32165.html',
        'tid.html',
    ]:
        yield check_parse_user_arts, name


def check_parse_user_arts(name):
    with open(os.path.join(CURRENT_PATH, name), 'rb') as f:
        sel = Selector(text=f.read(), type='html')
    assert_greater(len(list(parse_user_arts(sel))), 0)
