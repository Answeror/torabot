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
            cookies=request.get('cookies', requests.cookies.RequestsCookieJar()),
            data=request.get('body', '')
        ).prepare()
        return {
            'uri': request['uri'],
            'headers': dict(prepared.headers),
            'method': prepared.method,
            'body': prepared.body,
            'payload': request.get('payload'),
            'env': self.env.name
        }

    @property
    def default_timeout(self):
        from ...local import get_current_conf
        return get_current_conf()['TORABOT_SPY_TIMEOUT']

    def __call__(self, request, timeout=None, sync_on_expire=False):
        if isuri(request):
            request = {'uri': request}
        query = mod('onereq').search(
            text=jsonpickle.encode(self.prepare(request)),
            timeout=self.default_timeout if timeout is None else timeout,
            sync_on_expire=sync_on_expire,
            backend=Redis()
        )
        if query is None:
            raise Exception('request {} failed, args: {}'.format(self.name, request))
        return query.result


def isuri(request):
    return isinstance(request, str)
