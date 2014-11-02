import json
from nose.tools import assert_equal
from .. import bilibili
from . import TestSuite


class TestRegular(TestSuite):

    def test_regular(self):
        def gen(query, d_true):
            (kind, query), d = bilibili.regular(query), bilibili.parse(query)
            assert_equal(kind, bilibili.name)
            assert_equal(json.loads(query), d)
            assert_equal(d, d_true)

        yield gen, 'foo', dict(method='sp', title='foo')
        yield gen, '{"method": "sp", "title": "foo"}', dict(method='sp', title='foo')
        yield gen, '{"method": "bangumi"}', dict(method='bangumi')
        yield gen, '{"method": "user", "user_id": "0"}', dict(method='user', user_id='0')
