import json
from nose.tools import assert_greater
from .... import make
from ....core.mod import mod
from ...ut import need_scrapyd
from .. import name


@need_scrapyd
def test_spy_rss():
    app = make()
    with app.test_client():
        uri = 'http://www.yyets.com/rss/feed/?area=%E7%BE%8E%E5%9B%BD'
        d = mod(name).spy(json.dumps(dict(method='rss', uri=uri)), 60)
        assert_greater(len(d.arts), 0)
        d = mod(name).spy(uri, 60)
        assert_greater(len(d.arts), 0)
