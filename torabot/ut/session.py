from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


@contextmanager
def makesession(commit=False, **kargs):
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
    else:
        assert False, 'must provide engine, connection or config'

    Session = sessionmaker(bind=bind)
    session = Session(**kargs)
    try:
        yield session
        if commit:
            session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


@contextmanager
def makeappsession(commit=False, **kargs):
    from flask import current_app
    with makesession(current_app.config, commit=commit, **kargs) as session:
        yield session
