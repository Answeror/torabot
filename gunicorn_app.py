import os
from torabot import make
from werkzeug.contrib.fixers import ProxyFix


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))

app = make(
    instance_path=os.path.join(CURRENT_PATH, 'data'),
    instance_relative_config=True,
)
app.wsgi_app = ProxyFix(app.wsgi_app)
