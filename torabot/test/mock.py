from httmock import all_requests
from . import freeze
from logbook import Logger
import requests
from nose.tools import assert_in


log = Logger(__name__)


def real(req):
    mockrequests.disable = True
    try:
        return requests.Session().send(req)
    finally:
        mockrequests.disable = False


@freeze.all_requests
def mockrequests(url, req):
    d = freeze.load()
    if freeze.reqmd5(req) not in d:
        log.info('{} not in cache, fetch now', freeze.freezereq(req))
        freeze.append(req, real(req))
        d = freeze.load()
        assert_in(freeze.reqmd5(req), d)
    return d[freeze.reqmd5(req)][1]
