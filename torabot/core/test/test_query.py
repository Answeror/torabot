from nose.tools import assert_equal
from ..query import query
from . import g
from .spider import UsotukiyaSpider as Spider


class TestQuery(object):

    def setup(self):
        self.spider = Spider()
        self.trans = g.connection.begin_nested()

    def teardown(self):
        self.trans.rollback()

    def query(self, *args, **kargs):
        kargs.update(spider=self.spider, conn=g.connection)
        return query(*args, **kargs)

    def test_query(self):
        assert_equal(len(self.query('大嘘')), 8)

    def test_paged_query(self):
        a_2_7 = self.query('大嘘', begin=2, end=7)
        a_5_7 = self.query('大嘘', begin=5, end=7)
        assert_equal(len(a_2_7), 5)
        assert_equal(len(a_5_7), 2)
        assert_equal(
            [art.uri for art in a_2_7[3:4]],
            [art.uri for art in a_5_7[:1]]
        )

    def test_paged_query_twice(self):
        a_2_7 = self.query('大嘘', begin=2, end=7)
        a_5_7 = self.query('大嘘', begin=5, end=7)
        a_2_7 = self.query('大嘘', begin=2, end=7)
        a_5_7 = self.query('大嘘', begin=5, end=7)
        assert_equal(len(a_2_7), 5)
        assert_equal(len(a_5_7), 2)
        assert_equal(
            [art.uri for art in a_2_7[3:4]],
            [art.uri for art in a_5_7[:1]]
        )

    def test_paged_query_futher(self):
        self.query('大嘘', begin=2, end=5)
        a_5_7 = self.query('大嘘', begin=5, end=7)
        assert_equal(len(a_5_7), 2)
