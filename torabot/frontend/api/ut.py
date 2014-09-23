from flask import current_app
from logbook import Logger
from ... import celery


log = Logger(__name__)


def make(gist, args):
    log.info('make {} with {}', gist, args)
    return celery.make_source.apply_async(
        kwargs=dict(gist=gist, args=args),
        expires=current_app.config['TORABOT_MAKE_SOFT_TIMEOUT'],
        time_limit=current_app.config['TORABOT_MAKE_TIMEOUT'],
        soft_time_limit=current_app.config['TORABOT_MAKE_SOFT_TIMEOUT']
    ).get(interval=0.1)
