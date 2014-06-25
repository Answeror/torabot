import json
import base64
from nose.tools import assert_in, assert_equal
from .... import make
from ...ut import need_scrapyd
from .. import Onereq


@need_scrapyd
def test_spy_uri():
    app = make()
    with app.app_context():
        d = Onereq.instance.spy('http://httpbin.org/get', 60)
        for key in ['status', 'headers', 'body']:
            assert_in(key, d)
        assert base64.b64decode(d['body']).decode('ascii')


@need_scrapyd
def test_spy_payload():
    app = make()
    with app.app_context():
        payload = 'foo'
        d = Onereq.instance.spy(json.dumps({
            'uri': 'http://httpbin.org/get',
            'payload': payload
        }), 60)
        assert_equal(d['payload'], payload)
