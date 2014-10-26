from nose.tools import assert_equal
from ...ut.async_test_tools import with_event_loop
from ...db import db
from .. import core
from . import TestSuite, with_fake_tora_mod


class TestSearch(db.SandboxTestSuiteMixin, TestSuite):

    @with_event_loop
    @with_fake_tora_mod
    def test_search(self):
        query = yield from core.search(
            kind='tora',
            text='大嘘',
            bind=db.bind
        )
        assert_equal(query.kind, 'tora')
        assert_equal(query.text, '大嘘')
        assert query.result
