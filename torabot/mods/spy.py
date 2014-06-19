from logbook import Logger
from redis import Redis
import json
import requests
from datetime import datetime, timedelta
from redis_lock import Lock
from ..ut.bunch import bunchr
from ..ut.time import TIME_FORMAT
from ..core.local import get_current_conf
from ..spy.query import hash as hash_query
from .errors import ExpectedError


log = Logger(__name__)
redis = Redis()


class SpyTimeoutError(Exception):
    pass


def lives(kind):
    r = requests.get('http://localhost:6800/listjobs.json?project=%s' % kind)
    if not r.ok or r.json()['status'] != 'ok':
        return 0
    return len(r.json()['running']) + len(r.json()['pending'])


def prepare(kind, query, timeout, slaves, options):
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
                    **options
                )
            )
            if not r.ok or r.json()['status'] != 'ok':
                log.info('start {} slave failed', kind)
                return False
    return True


def merge_options(kind, options):
    conf = get_current_conf()
    prefix = 'TORABOT_MOD_%s_SPY_' % kind.upper()
    keys = [key for key in conf.keys() if key.startswith(prefix)]
    d = {key[len(prefix):].lower(): conf[key] for key in keys}
    d.update(options)
    return d


def spy(kind, query, timeout, slaves, options={}):
    options = merge_options(kind, options)
    log.debug('spy {} for {} with options: {}', query, kind, options)

    if not prepare(kind, query, timeout, slaves, options):
        raise Exception('spy %s for %s failed not prepared' % (kind, query))

    redis.rpush('torabot:spy:%s' % kind, query.encode('utf-8'))
    while True:
        resp = redis.blpop(
            'torabot:spy:%s:%s:items' % (kind, hash_query(query)),
            timeout=timeout
        )
        if not resp:
            break

        r = json.loads(resp[1].decode('utf-8'))
        if datetime.strptime(r['ctime'], TIME_FORMAT) + timedelta(seconds=int(timeout)) < datetime.utcnow():
            continue
        r = r['result']
        if r.get('ok', True):
            return bunchr(r)
        message = r.get('message', 'no error message')
        if r.get('expected', False):
            raise ExpectedError(message)
        raise Exception('spy %s for %s failed: %s' % (kind, query, message))

    raise SpyTimeoutError('spy %s for %s timeout')
