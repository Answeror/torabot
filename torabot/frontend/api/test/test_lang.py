import json
import aiohttp
from nose.tools import assert_equal
from ....ut.async_test_tools import with_event_loop
from ....alask.testing import serving
from ....alask import Alask
from .. import bp


app = Alask(__name__)
app.register_blueprint(bp)


@with_event_loop
@serving(app)
def test_ping(host, port):
    resp = yield from aiohttp.request(
        method='GET',
        url='http://{}:{}/ping'.format(host, port)
    )
    data = yield from resp.read()
    assert_equal(data.decode('ascii'), 'pong')


@with_event_loop
@serving(app)
def test_make(host, port):
    resp = yield from aiohttp.request(
        method='POST',
        url='http://{}:{}/make.json'.format(host, port),
        data=json.dumps({
            'files': {
                'main.json': {
                    'content': json.dumps({
                        '@json_encode': {
                            'foo': 'bar'
                        }
                    })
                }
            }
        }).encode('ascii')
    )
    assert_equal(resp.status, 200)
    data = yield from resp.read()
    assert_equal(json.loads(data.decode('ascii')), {'foo': 'bar'})
