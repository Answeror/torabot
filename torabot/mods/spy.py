import os
import shutil
from logbook import Logger
import json
import requests
from datetime import datetime, timedelta
from redis_lock import Lock
from ..ut.bunch import bunchr
from ..ut.time import TIME_FORMAT
from ..core.local import get_current_conf
from ..spy.query import hash as hash_query
from .errors import ExpectedError, SpyTimeoutError
from ..core.redis import redis


log = Logger(__name__)


def lives(kind):
    r = requests.get('http://localhost:6800/listjobs.json?project=%s' % kind)
    if not r.ok or r.json()['status'] != 'ok':
        return 0
    return len(r.json()['running']) + len(r.json()['pending'])


def jobids(kind):
    root = os.path.join('logs', kind, kind)
    return [name[:-4] for name in list(os.listdir(root))]


def prepare(kind, query, timeout, slaves, options):
    with Lock(redis, 'torabot:temp:spy_prepare'):
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
                    life=2 * timeout,
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


def get_all_jobids_and_copy(kind):
    ids = jobids(kind)
    copy_logs(kind, ids)
    return ids


def copy_logs(kind, jobids):
    result = []
    for id in jobids:
        root = os.path.join(get_current_conf()['TORABOT_DATA_PATH'], 'scrapy')
        if not os.path.exists(root):
            os.makedirs(root)
        filename = id + '.log'
        source = os.path.join('logs', kind, kind, filename)
        if os.path.exists(source):
            shutil.copyfile(
                source,
                os.path.join(root, filename)
            )
            result.append(id)
    return result


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
            log.debug('got expired spy result of ({}, {})', kind, query)
            continue
        r = r['result']
        if r.get('ok', True):
            return bunchr(r)
        message = r.get('message', 'no error message')
        if r.get('expected', False):
            raise ExpectedError(message)
        raise Exception('spy {} for {} failed: {}'.format(
            kind,
            query,
            message,
        ))

    raise SpyTimeoutError('spy {} for {} timeout'.format(
        kind,
        query,
    ))
