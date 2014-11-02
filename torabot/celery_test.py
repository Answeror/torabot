from .celery import celery, app
from .db import db
from .ut.redis import redis
from .ut.request import request
from .core import core


celery.config_from_object('torabot.ut.test_config')
app.config.from_object('torabot.ut.test_config')
db.init_app(app)
redis.init_app(app)
request.init_app(app)
core.init_app(app)
