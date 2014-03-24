from celery.schedules import crontab

# flask
SECRET_KEY = 'test'

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
        'schedule': crontab(minute='*/15'),  # sync every 5 minutes
    },
    'notice': {
        'task': 'torabot.celery.notice_all',
        'schedule': crontab(minute='*/15'),  # notice every 5 minutes
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
TORABOT_QUERY_EXPIRE = 15 * 60

# mod
TORABOT_DEFAULT_MOD = 'tora'
TORABOT_MOD_TORA_TRANSLATE = True
# pixiv cookies
# TORABOT_MOD_PIXIV_SPY_PHPSESSID = ''
TORABOT_MOD_PIXIV_SPY_MAX_ARTS = 12
