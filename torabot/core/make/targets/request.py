import requests
import jsonpickle
from ...backends.redis import Redis
from ...mod import mod
from .base import Base


class Target(Base):

    unary = False

    def prepare(self, request):
        prepared = requests.Request(
            url=request['uri'],
            method=request.get('method', 'GET'),
            headers=request.get('headers', {}),
            cookies=request.get('cookies', requests.cookies.RequestsCookieJar())
        ).prepare()
        return {
            'uri': request['uri'],
            'headers': dict(prepared.headers),
            'method': prepared.method,
            'payload': request.get('payload'),
        }

    def __call__(self, request, timeout=10, sync_on_expire=False):
        if isuri(request):
            request = {'uri': request}
        query = mod('onereq').search(
            text=jsonpickle.encode(self.prepare(request)),
            timeout=timeout,
            sync_on_expire=sync_on_expire,
            backend=Redis()
        )
        if query is None:
            raise Exception('request %s failed' % self.name)
        return query.result


def isuri(request):
    return isinstance(request, str)
