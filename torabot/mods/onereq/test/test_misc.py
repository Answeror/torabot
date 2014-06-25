import json
from .... import make
from ...ut import need_scrapyd
from .. import Onereq


@need_scrapyd
def test_sync_on_expire():
    app = make()
    with app.app_context():
        assert Onereq.instance.sync_on_expire('http://google.com')
        assert not Onereq.instance.sync_on_expire(json.dumps({
            'uri': 'http://google.com',
            'options': {'sync_on_expire': False}
        }))
