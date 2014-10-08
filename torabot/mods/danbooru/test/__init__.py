from ....core.connection import ContextFixture


g = ContextFixture()


def setup_module():
    g.setup()


def teardown_module():
    g.teardown()
