from celery.schedules import crontab


TORABOT_CONNECTION_STRING = (
    'postgresql+psycopg2://{0}:{0}@localhost/{0}'
    .format('torabot-dev')
)
TORABOT_SYNC_THREADS = 32
TORABOT_EMAIL_HEAD = 'torabot notice'

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
        'schedule': crontab(minute='*/5'),  # sync every 5 minutes
    },
    'notice': {
        'task': 'torabot.celery.notice_all',
        'schedule': crontab(minute='*/5'),  # notice every 5 minutes
    }
}
