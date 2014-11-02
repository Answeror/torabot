import json
from nose.tools import assert_equal
from ...ut.async_test_tools import with_event_loop
from .. import lang
from . import TestSuite


class TestRun(TestSuite):

    @with_event_loop
    def test_run_json_gist(self):
        result = yield from lang.run_json_gist(
            '9f9eca62ecdde1460052',
            {
                'string': 'foo',
                'int': 42
            }
        )
        assert_equal(result, {
            'string': 'foo',
            'int': 42
        })

    @with_event_loop
    def test_run_dict(self):
        result = yield from lang.run_dict({
            'files': {
                'main.json': {
                    'content': json.dumps({
                        '@json_encode': {
                            'foo': 'bar'
                        }
                    })
                }
            }
        })
        assert_equal(json.loads(result), {'foo': 'bar'})
