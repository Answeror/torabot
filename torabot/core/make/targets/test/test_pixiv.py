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
            json.loads(read('pixiv.json'))
        )
        assert_equal(len(json.loads(result)['arts']), 20)
        query = {
            'text': 'pixiv',
            'mtime': 0,
            'result': {
                'arts': json.loads(result)['arts'][:13]
            }
        }
        result = {
            'arts': json.loads(result)['arts'][10:]
        }
        changes = Target.run(
            Env(CURRENT_PATH),
            {
                "@eval": {
                    "@js": [
                        {"text<": "pixiv.js"},
                        ["main", query, result]
                    ]
                }
            }
        )
        assert_equal(len(changes), 7)
