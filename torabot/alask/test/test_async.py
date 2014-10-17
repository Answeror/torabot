import time
import asyncio
import aiohttp
from nose.tools import assert_less
from ...ut.async_test_tools import with_event_loop
from ..testing import serving
from .. import Alask


app = Alask(__name__)


@app.route('/')
def index():
    yield from asyncio.sleep(1)
    return ''


@with_event_loop
@serving(app)
def test_async_quick(host, port):
    start = time.time()
    yield from asyncio.wait([
        aiohttp.request('GET', 'http://{}:{}'.format(host, port))
        for x in range(3)
    ])
    assert_less(abs(time.time() - start - 1), .1)
