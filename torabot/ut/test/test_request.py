import json
from nose.tools import assert_equal
from unittest.mock import patch
from ...app import App
from ..request import request
from ..async_test_tools import with_event_loop


app = App(__name__)
request.init_app(app)


@with_event_loop
def test_get():
    with app.app_context():
        with patch('torabot.ut.request.set_cache') as set_cache:
            resp = yield from request.get(
                'http://httpbin.org/get?foo=bar',
                cache_life=0
            )
            assert not set_cache.called
        data = yield from resp.read()
        assert_equal(
            json.loads(data.decode('ascii'))['args'],
            {'foo': 'bar'}
        )
