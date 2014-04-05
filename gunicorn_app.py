from logbook.compat import redirect_logging
redirect_logging()

import os
from torabot import make
from torabot.core.log import RedisPub


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))

with RedisPub():
    app = make(
        instance_path=os.path.join(CURRENT_PATH, 'data'),
        instance_relative_config=True,
    )

from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)
