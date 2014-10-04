import asyncio
from functools import wraps


def with_event_loop(f):
    @wraps(f)
    def g(*args, **kargs):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.coroutine(f)(*args, **kargs))
    return g
