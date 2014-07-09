from time import time
from functools import wraps, partial
from logbook import Logger, Processor


log = Logger(__name__)


def exguard(f):
    @wraps(f)
    def g(*args, **kargs):
        try:
            return f(*args, **kargs)
        except:
            log.exception('{} failed', f.__name__)
    return g


def timeguard(f):
    @wraps(f)
    def g(*args, **kargs):
        start = time()
        try:
            return f(*args, **kargs)
        finally:
            log.info('{} takes {} seconds', f.__name__, time() - start)

    return g


def inject_func(name, args, kargs, record):
    context = record.extra.get('context', {})
    func = context.get('func', [])
    func.append({
        'name': name,
        'args': args,
        'kargs': kargs
    })
    context['func'] = func
    record.extra['context'] = context


def func_log_injected(f):
    @wraps(f)
    def g(*args, **kargs):
        with Processor(partial(
            inject_func,
            f.__name__,
            args,
            kargs
        )).threadbound():
            return f(*args, **kargs)
    return g


def time_logged(f):
    @wraps(f)
    def g(*args, **kargs):
        start = time()
        try:
            return f(*args, **kargs)
        finally:
            log.info('{} takes {} seconds', f.__name__, time() - start)

    return g
