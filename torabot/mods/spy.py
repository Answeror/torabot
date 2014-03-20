from logbook import Logger
from redis import Redis
import json
from hashlib import md5
from ..ut.bunch import bunchr
import requests
from redis_lock import Lock


log = Logger(__name__)
redis = Redis()


def lives(kind):
    r = requests.get('http://localhost:6800/listjobs.json?project=%s' % kind)
    if not r.ok or r.json()['status'] != 'ok':
        return 0
    return len(r.json()['running']) + len(r.json()['pending'])


def prepare(kind, query, timeout, slaves):
    with Lock(redis, 'torabot:core:spy:prepare'):
        while lives(kind) < slaves:
            log.info(
                'not enough {} slaves ({} < {}), start one',
                kind,
                lives(kind),
                slaves
            )
            r = requests.post(
                'http://localhost:6800/schedule.json',
                data=dict(
                    project=kind,
                    spider=kind,
                    life=timeout,
                )
            )
            if not r.ok or r.json()['status'] != 'ok':
                log.info('start {} slave failed', kind)
                return False
    return True


def spy(kind, query, timeout, slaves):
    if not prepare(kind, query, timeout, slaves):
        raise Exception('spy %s for %s failed not prepared' % (kind, query))

    redis.rpush('torabot:spy:%s' % kind, query.encode('utf-8'))
    id = md5(query.encode('utf-8')).hexdigest()
    resp = redis.blpop('torabot:spy:%s:%s:items' % (kind, id), timeout=timeout)
    if resp:
        r = json.loads(resp[1].decode('ascii'))
        if r.get('ok', True):
            return bunchr(r)

    raise Exception('spy %s for %s failed' % (kind, query))
