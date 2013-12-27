import os
import sys


CURRENT_PATH = os.path.dirname(__file__)

sys.path.insert(
    0,
    os.path.abspath(os.path.join(CURRENT_PATH, '..', '..'))
)


from torabot.spider import fetch_and_parse_all
from httmock import HTTMock
import requests
import pickle
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


def append(req, resp):
    path = os.path.join(CURRENT_PATH, 'frozenreqs.pkl')
    if not os.path.exists(path):
        d = {}
    else:
        with open(path, 'rb') as f:
            d = pickle.loads(f.read())
    d[reqmd5(req)] = (freezereq(req), freezeresp(resp))
    with open(path, 'wb') as f:
        f.write(pickle.dumps(d))


def reqmd5(req):
    from hashlib import md5
    m = md5()
    m.update(pickle.dumps(freezereq(req)))
    return m.hexdigest()


def main():
    from pprint import pprint
    with HTTMock(freeze):
        pprint(fetch_and_parse_all('大嘘'))


if __name__ == '__main__':
    import sys
    sys.exit(main())
