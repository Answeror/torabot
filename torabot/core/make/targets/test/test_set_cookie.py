import os
import jsonpickle
from nose.tools import assert_equal, assert_in
from ...envs.fs import Env
from ..set_cookie import Target


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


def test_set_cookie():
    env = Env(root=CURRENT_PATH)
    target = Target(env=env)
    request = jsonpickle.decode(target(
        request=jsonpickle.encode({'uri': 'http://foo.bar'}),
        set_cookie='foo=bar'
    ))
    assert_in('cookies', request)
    assert_equal(request['cookies']['foo'], 'bar')
