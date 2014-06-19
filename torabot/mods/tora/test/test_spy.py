from nose.tools import assert_equal
from .... import make
from ....core.mod import mod
from ...ut import need_scrapyd
from .. import name


@need_scrapyd
def test_spy_rss():
    app = make()
    with app.app_context():
        for query in [
            'CLASSIC MILK+PEACE and ALIEN',
            'Beyond the SKY 混沌',
        ]:
            d = mod(name).spy(query, 60)
            assert_equal(d.total, 0)
            assert_equal(len(d.arts), 0)
