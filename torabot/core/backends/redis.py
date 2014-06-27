import pickle
from datetime import datetime
from hashlib import md5
from ...ut.bunch import bunchr
from ..redis import redis
from .base import Backend


class Redis(Backend):

    def has_query_bi_kind_and_text(self, kind, text):
        return redis.exists(encode(kind, text))

    def get_query_bi_kind_and_text(self, kind, text):
        q = redis.get(encode(kind, text))
        if q:
            return bunchr(pickle.loads(q))

    def set_next_sync_time_bi_kind_and_text(self, kind, text, time):
        ret = redis.expire(
            encode(kind, text),
            (time - datetime.utcnow()).seconds
        )
        if not ret:
            raise Exception('set next sync time of %s for %s failed' % (kind, text))

    def get_or_add_query_bi_kind_and_text(self, kind, text):
        id = encode(kind, text)
        q = redis.get(id)
        if q:
            q = pickle.loads(q)
        else:
            ctime = datetime.utcnow()
            q = {
                'id': id,
                'kind': kind,
                'text': text,
                'result': {},
                'ctime': ctime,
                'mtime': ctime,
                'next_sync_time': None
            }
            redis.set(id, pickle.dumps(q))
        return bunchr(q)

    def touch_query_bi_id(self, id):
        q = pickle.loads(redis.get(id))
        q['mtime'] = datetime.utcnow()
        redis.set(id, pickle.dumps(q))

    def add_one_query_changes(self, id, changes):
        if list(changes):
            assert False, 'not implemented'

    def set_query_result(self, id, result):
        q = pickle.loads(redis.get(id))
        q['result'] = result
        redis.set(id, pickle.dumps(q))

    def is_query_active_bi_id(self, id):
        return True

    def set_next_sync_time(self, id, time):
        ret = redis.expire(
            id,
            (time - datetime.utcnow()).seconds
        )
        if not ret:
            raise Exception('set next sync time of %s failed' % id)


def encode(kind, text):
    return 'torabot:backend:%s:%s' % (kind, md5(text.encode('utf-8')).hexdigest())
