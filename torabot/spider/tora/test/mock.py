import requests
from logbook import Logger
from nose.tools import assert_in
from time import sleep
from bs4 import BeautifulSoup as BS
from . import freeze
from .. import check_busy


log = Logger(__name__)


def busy(data):
    soup = BS(data, 'html5lib')
    return check_busy(soup)


def real(req):
    mockrequests.disable = True
    try:
        time = 1
        while True:
            try:
                r = requests.Session().send(req)
                if r.ok and not busy(r.content):
                    return r
                else:
                    raise Exception('request failed')
            except:
                log.info('request to {} failed, sleep {} seconds', req.url, time)
            sleep(time)
            time += time
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
