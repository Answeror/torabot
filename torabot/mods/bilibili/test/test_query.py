import json
from nose.tools import assert_equal
from ..query import standard_query


def test_standard_query():
    def gen(query, d_true):
        query, d = standard_query(query)
        assert_equal(json.loads(query), d)
        assert_equal(d, d_true)

    yield gen, 'foo', dict(method='sp', title='foo')
    yield gen, '{"method": "sp", "title": "foo"}', dict(method='sp', title='foo')
    yield gen, '{"method": "bangumi"}', dict(method='bangumi')
    yield gen, '{"method": "user", "user_id": "0"}', dict(method='user', user_id='0')
