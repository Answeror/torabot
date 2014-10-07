from functools import wraps
from asyncio import get_event_loop, coroutine
from ...ut.async_test_tools import with_event_loop
from .. import app


def with_async_web(f):
    @with_event_loop
    @wraps(f)
    def g(*args, **kargs):
        host = '127.0.0.1'
        port = 5000
        server = yield from app.make_server(host, port, get_event_loop())
        try:
            return (yield from coroutine(f)(host, port, *args, **kargs))
        finally:
            server.close()
    return g
