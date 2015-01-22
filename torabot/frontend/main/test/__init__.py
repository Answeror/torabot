from ....celery import celery
from ....app import App
from ....ut.testing import app_test_suite
from ....core import core
from ....db import db
from ... import frontend


app = App(__name__)
app.config.from_object('torabot.ut.test_config')
core.init_app(app)
frontend.init_app(app)
celery.config_from_object('torabot.ut.test_config')


class TestSuite(db.SandboxTestSuiteMixin, app_test_suite(app)):
    pass
