import os
from nose.tools import assert_equal
from ...envs.fs import Env
from ..request import Target as RequestTarget
from ..set_cookie import Target as SetCookieTarget


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


def test_request():
    env = Env(root=CURRENT_PATH)
    targets = {
        'set_cookie': SetCookieTarget(env=env),
        'request': RequestTarget(env=env)
    }
    request = {
        'uri': 'http://httpbin.org/cookies',
        'headers': {'Cookie': 'bar=1'}
    }
    prepared = targets['request'].prepare(request=request)
    assert_equal(prepared['headers']['Cookie'], 'bar=1')
    request = targets['set_cookie'](request, set_cookie='foo=bar')
    prepared = targets['request'].prepare(request=request)
    assert_equal(
        sorted(prepared['headers']['Cookie'].split('; ')),
        ['bar=1', 'foo=bar']
    )
