from celery.schedules import crontab
import os


# flask
SECRET_KEY = 'test'
CACHE_TYPE = 'simple'
TRAP_BAD_REQUEST_ERRORS = True

# celery
BROKER_URL = 'redis://'
CELERY_RESULT_BACKEND = 'redis://'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERYBEAT_SCHEDULE = {
    'sync': {
        'task': 'torabot.celery.sync_all',
        'schedule': crontab(minute='*/15'),  # sync every 15 minutes
    },
    'notice': {
        'task': 'torabot.celery.notice_all',
        'schedule': crontab(minute='*/5'),  # notice every 5 minutes
    },
    'log_to_file': {
        'task': 'torabot.celery.log_to_file',
        'schedule': crontab(minute='*/1'),  # log every 1 minutes
    }
}

TORABOT_CONNECTION_STRING = (
    'postgresql+psycopg2://{0}:{0}@localhost/{0}'
    .format('torabot-dev')
)
TORABOT_SYNC_THREADS = 32
TORABOT_EMAIL_HEAD = 'torabot notice'
TORABOT_SPY_TIMEOUT = 300
TORABOT_SPY_SLAVES = 1
TORABOT_NOTICE_ROOM = 16
TORABOT_PAGE_ROOM = 16
TORABOT_QUERY_EXPIRE = 15 * 60
TORABOT_BUBBLE_LOG = True
TORABOT_DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data')
TORABOT_ADVANCED_SEARCH_CACHE_TIMEOUT = 600

# mod
TORABOT_DEFAULT_MOD = 'tora'
TORABOT_MOD_TORA_TRANSLATE = True
# pixiv cookies
# TORABOT_MOD_PIXIV_SPY_PHPSESSID = ''
TORABOT_MOD_PIXIV_SPY_MAX_ARTS = 12
