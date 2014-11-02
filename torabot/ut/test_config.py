DEBUG = True
TORABOT_QUERY_EXPIRE = 0

# celery
BROKER_URL = 'redis://'
CELERY_RESULT_BACKEND = 'redis://'
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_TIMEZONE = 'UTC'

from logbook import Logger

log = Logger(__name__)

try:
    from .test_config_private import *
except:
    log.warning('No test_config_private provided')
