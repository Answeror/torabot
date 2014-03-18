import subprocess as sp
from logbook import Logger
from redis import Redis
import json
from ..ut.bunch import bunchr


log = Logger(__name__)
redis = Redis()


def spy(kind, query, timeout):
    sp.check_call([
        'curl',
        'http://localhost:6800/schedule.json',
        '-d', 'project=torabot',
        '-d', 'spider=%s' % kind,
        '-d', 'query=%s' % query,
    ])
    resp = redis.blpop('torabot:spy:%s:items' % kind, timeout=timeout)
    if resp:
        r = json.loads(resp[1].decode('ascii'))
        if r.get('ok', True):
            return bunchr(r)
    raise Exception('spy %s for %s failed' % (kind, query))
