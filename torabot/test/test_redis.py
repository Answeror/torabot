from ..redis import redis
from nose.tools import assert_equal
import pickle


class TestRedis(object):

    def setup(self):
        redis.delete('foo')

    def teardown(self):
        redis.delete('foo')

    def test_redis_rpush(self):
        redis.rpush('foo', pickle.dumps(42))
        assert_equal(pickle.loads(redis.blpop('foo', timeout=1)[1]), 42)
