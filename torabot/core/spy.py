from logbook import Logger
from redis import Redis
import json
from hashlib import md5
from ..ut.bunch import bunchr
import requests
from redis_lock import Lock


log = Logger(__name__)
redis = Redis()


def runnings(kind):
    r = requests.get('http://localhost:6800/listjobs.json?project=%s' % kind)
    if not r.ok or r.json()['status'] != 'ok':
        return 0
    return len(r.json()['running'])


def prepare(kind, query, timeout, **kargs):
    with Lock(redis, 'torabot:core:spy:prepare'):
        while runnings(kind) < kargs.get('slaves', 1):
            r = requests.post(
                'http://localhost:6800/schedule.json',
                data=dict(
                    project=kind,
                    spider=kind,
                    life=timeout,
                )
            )
            if not r.ok or r.json()['status'] != 'ok':
                return False
    return True


def spy(kind, query, timeout, **kargs):
    if not prepare(kind=kind, query=query, timeout=timeout):
        raise Exception('spy %s for %s failed not prepared' % (kind, query))

    redis.rpush('torabot:spy:%s' % kind, query.encode('utf-8'))
    id = md5(query.encode('utf-8')).hexdigest()
    resp = redis.blpop('torabot:spy:%s:%s:items' % (kind, id), timeout=timeout)
    if resp:
        r = json.loads(resp[1].decode('ascii'))
        if r.get('ok', True):
            return bunchr(r)

    raise Exception('spy %s for %s failed' % (kind, query))
