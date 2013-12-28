from httmock import all_requests
from . import freeze


@all_requests
def mockrequests(url, req):
    d = freeze.load()
    for key in d:
        print(d[key][0])
    return freeze.load()[freeze.reqmd5(req)][1]
