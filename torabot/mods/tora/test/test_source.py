from nose.tools import assert_equal
from ....ut.async_test_tools import with_event_loop
from .. import tora
from . import TestSuite


class TestSource(TestSuite):

    @with_event_loop
    def test_rss(self):
        for query in [
            'CLASSIC MILK+PEACE and ALIEN',
            'Beyond the SKY 混沌',
        ]:
            d = yield from tora.source(query, 60)
            assert_equal(d.total, 0)
            assert_equal(len(d.arts), 0)
