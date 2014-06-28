import os
import json
from nose.tools import assert_equal
from ...envs.fs import Env
from ..jinja2 import Target


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


def test_jinja2():
    env = Env(root=CURRENT_PATH)
    target = Target(env=env, options={
        'name': 'torabot/get.jinja2',
        'kargs': {'key': 'foo'}
    })
    assert_equal(target(json.dumps({'foo': 'bar'})), '"bar"')
