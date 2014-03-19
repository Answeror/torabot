from logbook import Logger
from redis import Redis
import json
from hashlib import md5
from ..ut.bunch import bunchr
import requests


log = Logger(__name__)
redis = Redis()


def prepare(kind, query, timeout, **kargs):
    r = requests.get('http://localhost:6800/listjobs.json?project=%s' % kind)
    if r.ok and r.json()['status'] == 'ok':
        if len(r.json()['running']) >= kargs.get('slaves', 1):
            return True
        r = requests.post(
            'http://localhost:6800/schedule.json',
            data=dict(
                project=kind,
                spider=kind,
                life=timeout,
            )
        )
        if r.ok and r.json()['status'] == 'ok':
            return True
    return False


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
