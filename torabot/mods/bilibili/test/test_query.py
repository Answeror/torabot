import json
from nose.tools import assert_equal
from ..query import parse, regular


def test_standard_query():
    def gen(query, d_true):
        query, d = regular(query), parse(query)
        assert_equal(json.loads(query), d)
        assert_equal(d, d_true)

    yield gen, 'foo', dict(method='sp', title='foo')
    yield gen, '{"method": "sp", "title": "foo"}', dict(method='sp', title='foo')
    yield gen, '{"method": "bangumi"}', dict(method='bangumi')
    yield gen, '{"method": "user", "user_id": "0"}', dict(method='user', user_id='0')
