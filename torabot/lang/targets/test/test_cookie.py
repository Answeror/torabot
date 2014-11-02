import json
from nose.tools import assert_equal
from flask import current_app
from ....ut.async_test_tools import with_event_loop
from .. import Target
from .ut import make_fs_env
from . import TestSuite


class TestCookie(TestSuite):

    @with_event_loop
    def test_pixiv_with_cookie(self):
        result = yield from Target.run(
            make_fs_env(),
            {
                '@eval': {
                    '@js': [
                        {'text<': 'pixiv.js'},
                        [
                            current_app.config['TORABOT_TEST_PIXIV_USERNAME'],
                            current_app.config['TORABOT_TEST_PIXIV_PASSWORD']
                        ]
                    ]
                }
            }
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
        changes = yield from Target.run(
            make_fs_env(),
            {
                '@js': {
                    'code': {'text<': 'pixiv_changes.js'},
                    'func': 'changes',
                    'args': [query, result]
                }
            }
        )
        assert_equal(len(changes), 7)

    @with_event_loop
    def test_pixiv_without_cookie(self):
        result = yield from Target.run(
            make_fs_env(),
            {
                '@eval': {
                    '@js': [
                        {'text<': 'pixiv_without_cookie.js'},
                        [
                            current_app.config['TORABOT_TEST_PIXIV_USERNAME'],
                            current_app.config['TORABOT_TEST_PIXIV_PASSWORD']
                        ]
                    ]
                }
            }
        )
        assert_equal(len(json.loads(result)['arts']), 0)
