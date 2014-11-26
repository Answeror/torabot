import inspect
from functools import wraps


def return_list(func):
    if not inspect.isgeneratorfunction(func):
        return func

    @wraps(func)
    def wrapped(*args, **kargs):
        return list(func(*args, **kargs))

    return wrapped
