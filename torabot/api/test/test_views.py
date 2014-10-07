import json
from nose.tools import assert_equal
from ...ut.async_request import request
from .ut import with_async_web


@with_async_web
def test_ping(host, port):
    resp = yield from request(
        method='GET',
        url='http://{}:{}/ping'.format(host, port),
        cache_life=0
    )
    data = yield from resp.read()
    assert_equal(data.decode('ascii'), 'pong')


@with_async_web
def test_make(host, port):
    resp = yield from request(
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
        }).encode('ascii'),
        cache_life=0
    )
    assert_equal(resp.status, 200)
    data = yield from resp.read()
    assert_equal(json.loads(data.decode('ascii')), {'foo': 'bar'})
