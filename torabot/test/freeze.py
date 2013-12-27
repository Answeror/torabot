import os
import sys


CURRENT_PATH = os.path.dirname(__file__)
FROZEN_PATH = os.path.join(CURRENT_PATH, 'frozenreqs.pkl')

sys.path.insert(
    0,
    os.path.abspath(os.path.join(CURRENT_PATH, '..', '..'))
)


from torabot.spider import fetch_and_parse_all
from httmock import HTTMock
import requests
import pickle
import json
from functools import wraps


def all_requests(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if getattr(inner, 'disable', False):
            return
        return func(*args, **kwargs)
    return inner


def freezereq(req):
    return {
        'url': req.url,
        'method': req.method,
        'headers': dict(req.headers),
    }


def freezeresp(resp):
    return {
        'status_code': resp.status_code,
        'content': resp.content,
    }


@all_requests
def freeze(url, req):
    def real(req):
        freeze.disable = True
        try:
            return requests.Session().send(req)
        finally:
            freeze.disable = False

    resp = real(req)
    append(req, resp)
    return resp


def load():
    if not os.path.exists(FROZEN_PATH):
        d = {}
    else:
        with open(FROZEN_PATH, 'rb') as f:
            d = pickle.loads(f.read())
    return d


def append(req, resp):
    d = load()
    d[reqmd5(req)] = (freezereq(req), freezeresp(resp))
    with open(FROZEN_PATH, 'wb') as f:
        f.write(pickle.dumps(d))


def reqmd5(req):
    from hashlib import md5
    m = md5()
    m.update(json.dumps(freezereq(req), sort_keys=True).encode('utf-8'))
    return m.hexdigest()


def main():
    from pprint import pprint
    with HTTMock(freeze):
        pprint(fetch_and_parse_all('大嘘'))


if __name__ == '__main__':
    import sys
    sys.exit(main())
