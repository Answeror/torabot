from contextlib import contextmanager


@contextmanager
def ccontext(commit=False, **kargs):
    if 'engine' in kargs:
        conn = kargs['engine'].connect()
        del kargs['engine']
    elif 'connection' in kargs:
        conn = kargs['connection']
        del kargs['connection']
    elif 'config' in kargs:
        from sqlalchemy import create_engine
        conn = create_engine(kargs['config']['TORABOT_CONNECTION_STRING']).connect()
        del kargs['config']
    elif 'make' in kargs:
        conn = kargs['make']()
        del kargs['make']
    else:
        assert False, 'must provide engine, connection or config'

    try:
        trans = conn.begin()
        yield conn
        if commit:
            trans.commit()
    except:
        trans.rollback()
        raise
    finally:
        conn.close()


@contextmanager
def appccontext(commit=False, **kargs):
    from .engine import appengine
    with ccontext(commit=commit, engine=appengine(), **kargs) as conn:
        yield conn
