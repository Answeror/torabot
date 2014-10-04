import base64
import aiohttp
from logbook import Logger
from asyncio import coroutine, wait_for
from ...ut.async_local import local
from .base import Base


log = Logger(__name__)


class Target(Base):

    unary = False

    @property
    def default_timeout(self):
        return local.conf['TORABOT_SPY_TIMEOUT']

    def _prepare(self, request, context):
        if is_uri(request):
            request = {'uri': request}
        return dict(
            url=request['uri'],
            method=request.get('method', 'GET'),
            headers=request.get('headers', {}),
            cookies=request.get('cookies', {}),
            data=base64.b64decode(request.get('body', '')),
            connector=self._conn(context)
        )

    def _conn(self, name):
        '''TCP connection for Cookies sharing'''
        c = self.env.context.get(name)
        if c is None:
            c = aiohttp.TCPConnector(share_cookies=True)
            self.env.context[name] = c
        return c

    @coroutine
    def __call__(self, request, timeout=None, context=None):
        options = self._prepare(request, self.regular_context(context))
        log.debug('Request headers: {}', options['headers'])
        log.debug('Connection cookies: {}', options['connector'].cookies)
        resp = yield from wait_for(
            aiohttp.request(**options),
            self.default_timeout if timeout is None else timeout
        )
        log.debug('Response headers: {}', resp.headers)
        return {
            'status': resp.status,
            'headers': dict(resp.headers),
            'cookies': dict(resp.cookies),
            'body': base64.b64encode((yield from resp.read()))
        }


def is_uri(request):
    return isinstance(request, str)
