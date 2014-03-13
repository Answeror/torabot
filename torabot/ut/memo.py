from functools import wraps
from fn.iters import drop
from joblib import hash


def unary(f):
    @wraps(f)
    def g():
        if not hasattr(g, 'result'):
            g.result = f()
        return g.result
    return g


def value(x):
    def g(*args, **kargs):
        return x
    return g


def memo(f):
    d = {}

    @wraps(f)
    def inner(*args, **kargs):
        a = d.get(hash((args, kargs)))
        if a is None:
            a = d[hash((args, kargs))] = f(*args, **kargs)
        return a

    return inner


def gemo(f):
    d = {}

    @wraps(f)
    def inner(*args, **kargs):
        a = d.get(hash((args, kargs)))
        if a is None:
            a = d[hash((args, kargs))] = []
        yield from a
        for x in drop(len(a), f(*args, **kargs)):
            a.append(x)
            yield x

    return inner
