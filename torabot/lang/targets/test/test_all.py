import json
import feedparser
from flask import current_app
from nose.tools import assert_equal, assert_greater
from ....ut.async_test_tools import with_event_loop
from .. import Target
from .ut import make_fs_env, read
from . import TestSuite


class TestAll(TestSuite):

    @with_event_loop
    def test_toy(self):
        assert_equal((yield from Target.run(
            make_fs_env(),
            json.loads(read('toy.json'))
        )), 0)

    @with_event_loop
    def test_bgm_pm_task(self):
        result = yield from Target.run(
            make_fs_env(),
            {
                '@eval': {
                    '@js': [
                        {'text<': 'bgm_pm.js'},
                        [current_app.config['TORABOT_TEST_CHII_AUTH']]
                    ]
                }
            }
        )
        feed = feedparser.parse(result)
        assert not feed.bozo
        assert_greater(len(feed.entries), 0)

    @with_event_loop
    def test_bgm_comments_task(self):
        result = yield from Target.run(
            make_fs_env(),
            {
                '@eval': {
                    '@js': [
                        {'text<': 'bgm_comments.js'},
                        ['/group/topic/32268']
                    ]
                }
            }
        )
        feed = feedparser.parse(result)
        assert not feed.bozo
        assert_greater(len(feed.entries), 0)
