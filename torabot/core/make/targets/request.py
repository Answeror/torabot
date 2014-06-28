import requests
import jsonpickle
from ...backends.redis import Redis
from ...mod import mod
from .base import Base


class Target(Base):

    def prepare(self, request):
        if not isinstance(request, dict):
            request = jsonpickle.decode(request)
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

    def __call__(self, request):
        query = mod('onereq').search(
            text=jsonpickle.encode(self.prepare(request)),
            timeout=self.options.get('timeout', 10),
            sync_on_expire=self.options.get('sync_on_expire', False),
            backend=Redis()
        )
        if query is None:
            raise Exception('request %s failed' % self.name)
        return jsonpickle.encode(query.result)
