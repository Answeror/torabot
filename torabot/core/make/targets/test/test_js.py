import os
import json
from ..... import make
from ...envs.fs import Env
from .. import Target
from nose.tools import assert_equal


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


def read(name):
    with open(os.path.join(CURRENT_PATH, name), 'rb') as f:
        return f.read().decode('utf-8')


def test_pixiv():
    app = make()
    with app.app_context():
        result = Target.run(
            Env(CURRENT_PATH),
            json.loads(read('changes.json'))
        )
        assert_equal(result, ['c', 'd'])
