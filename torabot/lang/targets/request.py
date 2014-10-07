import base64
import aiohttp
from logbook import Logger
from asyncio import coroutine, wait_for
from ...ut.async_local import local
from ...ut.async_request import request
from .base import Base


log = Logger(__name__)


class Target(Base):

    unary = False

    @property
    def default_timeout(self):
        return local.conf['TORABOT_SPY_TIMEOUT']

    def _prepare(self, context=None, **kargs):
        options = dict(
            url=kargs['uri'],
            method=kargs.get('method', 'GET'),
            headers=kargs.get('headers', {}),
            cookies=kargs.get('cookies', {}),
            data=base64.b64decode(kargs.get('body', ''))
        )
        if context is not None:
            options['connector'] = self._conn(self.regular_context(context))
        return options

    def _conn(self, name):
        '''TCP connection for Cookies sharing'''
        c = self.env.context.get(name)
        if c is None:
            c = aiohttp.TCPConnector(share_cookies=True)
            self.env.context[name] = c
        return c

    @coroutine
    def stateless(self, *args, **kargs):
        return kargs['context'] is None

    @coroutine
    def __call__(self, uri, **kargs):
        options = self._prepare(uri=uri, **kargs)
        # log.debug('Request headers: {}', options['headers'])
        # if 'context' in kargs:
            # log.debug('Connection cookies: {}', options['connector'].cookies)
        resp = yield from wait_for(
            request(**options),
            timeout=kargs.get('timeout', self.default_timeout)
        )
        # log.debug('Response headers: {}', resp.headers)
        result = {
            'status': resp.status,
            'headers': dict(resp.headers),
            'cookies': dict(resp.cookies),
            'body': base64.b64encode((yield from resp.read())).decode('ascii')
        }
        if 'context' in kargs:
            result['context'] = {
                'name': kargs['context'],
                'cookies': dict(options['connector'].cookies)
            }
        return result
