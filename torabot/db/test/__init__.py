from ...ut.testing import app_test_suite
from ...app import App
from .. import db


app = App(__name__)
app.config.from_object(__name__)
db.init_app(app)


TestSuite = app_test_suite(app)
