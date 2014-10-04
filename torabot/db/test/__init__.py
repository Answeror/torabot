import logbook
from ...ut.bunch import Bunch
from .. import DatabaseFixture


g = DatabaseFixture()


def setup_module():
    g.setup()


def teardown_module():
    g.teardown()
