from httmock import all_requests
from . import freeze


@all_requests
def mockrequests(url, req):
    d = freeze.load()
    if freeze.reqmd5(req) not in d:
        raise Exception('{} not in cache'.format(freeze.freezereq(req)))
    return d[freeze.reqmd5(req)][1]
