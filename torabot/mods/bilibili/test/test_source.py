import json
from nose.tools import assert_equal, assert_in, assert_greater
from ....ut.async_test_tools import with_event_loop
from .. import bilibili
from . import TestSuite


class TestSource(TestSuite):

    @with_event_loop
    def test_spy_bangumi(self):
        d = yield from bilibili.source('{"method": "bangumi"}', 60)
        assert_in('content', d)

    @with_event_loop
    def test_spy_sp(self):
        d = yield from bilibili.source('{"method": "bangumi"}', 60)
        assert_equal(d['query']['method'], 'bangumi')
        title = d['content'][0]['title']
        d = yield from bilibili.source('{"method": "sp", "title": "%s"}' % title, 60)
        assert_in('sp', d)

    @with_event_loop
    def test_spy_user(self):
        d = yield from bilibili.source('{"method": "user", "user_id": "928123"}', 60)
        assert_in('posts', d)

    @with_event_loop
    def test_spy_username(self):
        d = yield from bilibili.source(json.dumps({
            'method': 'username',
            'username': '搬'
        }), 60)
        assert_greater(len(d['posts']), 0)
        d = yield from bilibili.source(json.dumps({
            'method': 'username',
            'username': '搬 搬'
        }), 60)
        assert_equal(len(d['posts']), 0)
        assert_greater(len(d['recommendations']), 0)

    @with_event_loop
    def test_spy_query(self):
        d = yield from bilibili.source(json.dumps({
            'method': 'query',
            'query': '东方'
        }), 60)
        assert_greater(len(d['posts']), 0)
