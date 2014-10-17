import asyncio
import aiohttp.wsgi
from functools import wraps


def serving(app):
    def wrap(f):
        @wraps(f)
        def g(*args, **kargs):
            host = '127.0.0.1'
            port = 5000
            loop = asyncio.get_event_loop()
            server = yield from loop.create_server(
                lambda: aiohttp.wsgi.WSGIServerHttpProtocol(
                    app,
                    debug=True,
                    readpayload=True
                ),
                host,
                port
            )
            try:
                return (yield from f(host, port, *args, **kargs))
            finally:
                server.close()
        return g
    return wrap
