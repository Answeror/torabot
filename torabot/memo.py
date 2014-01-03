from functools import wraps


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
