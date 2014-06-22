import json
from nose.tools import assert_greater
from .... import make
from ...ut import need_scrapyd
from .. import Gist


@need_scrapyd
def test_spy_id():
    app = make()
    with app.app_context():
        d = Gist.instance.spy(json.dumps(dict(method='id', id='5566446')), 60)
        assert_greater(len(d.files), 0)
        assert d.files[0].content
