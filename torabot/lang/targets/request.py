import base64
from asyncio import coroutine, wait_for
from ...ut.request import request
from .base import Base


class Target(Base):

    unary = False

    def _prepare_options(self, context=None, **kargs):
        options = dict(
            uri=kargs['uri'],
            method=kargs.get('method', 'GET'),
            headers=kargs.get('headers', {}),
            cookies=kargs.get('cookies', {}),
            data=base64.b64decode(kargs.get('body', '')),
            timeout=kargs.get('timeout')
        )
        return options

    def _get_session(self, name):
        session = self.env.context.get(name)
        if session is None:
            session = request.session(stateless=False)
            self.env.context[name] = session
        return session

    @coroutine
    def stateless(self, *args, **kargs):
        return kargs['context'] is None

    @coroutine
    def __call__(self, uri, **kargs):
        if 'context' in kargs:
            session = self._get_session(self.regular_context(kargs['context']))
        else:
            session = request.session(stateless=True)

        options = self._prepare_options(uri=uri, **kargs)
        resp = yield from session.fetch(**options)
        result = {
            'status': resp.status,
            'headers': dict(resp.headers),
            'cookies': dict(resp.cookies),
            'body': base64.b64encode((yield from resp.read())).decode('ascii')
        }
        if 'context' in kargs:
            result['context'] = {
                'name': kargs['context'],
                'cookies': dict(self._get_session(kargs['context']).connector.cookies)
            }
        return result
