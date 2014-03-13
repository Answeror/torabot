#from pprint import pprint
from nose.tools import assert_equal
from httmock import HTTMock
from .mock import mockrequests
from .const import USOTUKIYA
from .. import gen_arts


def test_gen_arts():
    with HTTMock(mockrequests):
        arts = list(gen_arts('大嘘'))
    #pprint(arts)
    assert_equal(arts, USOTUKIYA)
