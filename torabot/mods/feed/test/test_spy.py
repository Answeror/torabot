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
        uri = 'https://yande.re/post/atom'
        d = mod(name).spy(json.dumps(dict(method='uri', uri=uri)), 60)
        assert_greater(len(d.data.entries), 0)
        d = mod(name).spy(uri, 60)
        assert_greater(len(d.data.entries), 0)
