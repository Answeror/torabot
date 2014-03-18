import subprocess as sp
from logbook import Logger
from redis import Redis
import json


log = Logger(__name__)
redis = Redis()


def spy(kind, query):
    try:
        sp.check_call([
            'curl',
            'http://localhost:6800/schedule.json',
            '-d',
            'project=torabot',
            '-d',
            'spider=%s' % kind,
            'query=%s' % query
        ])
    except:
        log.exception('spy %s for %s failed' % (kind, query))
        return {}
    return json.loads(redis.blpop('torabot:spy:%s:items' % kind))
