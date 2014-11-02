from ...celery import celery
from ...app import App
from ...ut.testing import app_test_suite
from .. import lang


app = App(__name__)
app.config.from_object('torabot.ut.test_config')
lang.init_app(app)

celery.config_from_object('torabot.ut.test_config')

TestSuite = app_test_suite(app)
