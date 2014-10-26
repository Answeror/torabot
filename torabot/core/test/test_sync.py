from nose.tools import assert_equal
from ...ut.async_test_tools import with_event_loop
from ...db import db
from .. import core
from . import TestSuite, with_fake_tora_mod


class TestSync(db.SandboxTestSuiteMixin, TestSuite):

    @with_event_loop
    @with_fake_tora_mod
    def test_sync(self):
        yield from core.sync(kind='tora', text='大嘘')
        assert_equal((yield from db.get_query_count(db.connection)), 1)
