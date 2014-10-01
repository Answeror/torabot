import os
from nose.tools import assert_equal
from ...envs.fs import Env
from ..jinja2 import Target


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


def test_jinja2():
    env = Env(root=CURRENT_PATH)
    target = Target(env=env)
    assert_equal(target(
        template={'name': 'torabot/get.jinja2'},
        kargs={'value': {'foo': 'bar'}, 'key': 'foo'}
    ), '"bar"')
