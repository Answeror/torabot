from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker


@contextmanager
def ccontext(commit=False, **kargs):
    if 'engine' in kargs:
        bind = kargs['engine']
        del kargs['engine']
    elif 'connection' in kargs:
        bind = kargs['connection']
        del kargs['connection']
    elif 'config' in kargs:
        from sqlalchemy import create_engine
        bind = create_engine(kargs['config']['TORABOT_CONNECTION_STRING'])
        del kargs['config']
    elif 'make' in kargs:
        bind = kargs['make']()
        del kargs['make']
    else:
        assert False, 'must provide engine, connection or config'

    try:
        Session = sessionmaker(bind=bind)
        session = Session()
        yield ConnectionProxy(session)
        if commit:
            session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


@contextmanager
def appccontext(commit=False, **kargs):
    from .engine import appengine
    with ccontext(commit=commit, engine=appengine(), **kargs) as conn:
        yield conn


class ConnectionProxy(object):

    def __init__(self, session):
        self.session = session

    def execute(self, *args, **kargs):
        return self.session.connection().execute(*args, **kargs)
