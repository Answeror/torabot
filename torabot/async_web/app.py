from nose.tools import assert_greater_equal, assert_is_instance, assert_equal
from asyncio import iscoroutinefunction, coroutine, async, get_event_loop
from asyncio.futures import Future
from routes import Mapper
from aiohttp.server import ServerHttpProtocol
from logbook import Logger
import inspect
from .request import Request
from .response import Response


log = Logger(__name__)


class App(object):

    def __init__(self, name):
        self.name = name
        self.routes = Mapper(register=False)

    def route(self, path, **conditions):
        def wrap(f):
            if not iscoroutinefunction(f) and inspect.isgeneratorfunction(f):
                f = coroutine(f)
            self.routes.connect(path, _handler=f, conditions=conditions)
            return f
        return wrap

    def run(self, *, host='127.0.0.1', port=5000, loop=None):
        if loop is None:
            loop = get_event_loop()
        async(self.make_server(host, port, loop))
        log.info("Async web listening on http://{0}:{1}".format(host, port))
        loop.run_forever()

    def make_protocal(self):
        return Protocol(self)

    def make_server(self, host, port, loop):
        return loop.create_server(lambda: self.make_protocal(), host, port)

    @coroutine
    def handle_request(self, request, response):
        match = self.routes.match(request.path)
        if match is None:
            handler = handle_404
            request.kargs = {}
        else:
            handler = match.pop('_handler')
            request.kargs = remove_none_value(match)

        spec = inspect.getargspec(handler)
        kargs = {'request': request, 'response': response}
        argv = len(spec.args)
        assert_greater_equal(argv, 2)
        if argv > 2:
            kargs.update(request.kargs)

        if iscoroutinefunction(handler):
            rv = yield from handler(**kargs)
        else:
            rv = handler(**kargs)

        yield from self.handle_data(response, rv)

    @coroutine
    def handle_data(self, response, rv):
        if yields(rv):
            yield from rv
            if not response.finished:
                response.write_eof()
            return

        status_or_headers = headers = None
        if isinstance(rv, tuple):
            rv, status_or_headers, headers = rv + (None,) * (3 - len(rv))

        if rv is None:
            raise ValueError('View function did not return a response')

        if isinstance(status_or_headers, (dict, list)):
            headers, status_or_headers = status_or_headers, None

        if isinstance(rv, tuple):
            assert_equal(len(rv), 3)
            rv, status_orig, headers_orig = rv
            if status_or_headers is None:
                status_or_headers = status_orig
            headers_orig.update(headers)
            headers = headers_orig

        if status_or_headers is not None:
            assert_is_instance(status_or_headers, int)
            response.set_status(status_or_headers)

        if headers:
            for key, value in (
                headers.items() if isinstance(headers, dict) else headers
            ):
                response.add_header(key, value)

        assert_is_instance(rv, (str, bytes, bytearray))
        response.write(rv, unchunked=True)


class Protocol(ServerHttpProtocol):

    def __init__(self, app, **kargs):
        super().__init__(**kargs)
        self.app = app

    @coroutine
    def handle_request(self, request, payload):
        response = self.prepare_response(request)
        request = Request(request, payload)
        return (yield from self.app.handle_request(request, response))

    def prepare_response(self, request):
        return Response(self.writer, 200, request=request)


def remove_none_value(d):
    return {key: value for key, value in d.items() if value is not None}


def handle_404(request, response):
    return '', 404


def yields(value):
    return isinstance(value, Future) or inspect.isgenerator(value)
