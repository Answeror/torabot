from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


@contextmanager
def makesession(commit=False, **kargs):
    if 'engine' in kargs:
        bind = kargs['engine']
        del kargs['engine']
        Session = sessionmaker(bind=bind)
    elif 'connection' in kargs:
        bind = kargs['connection']
        del kargs['connection']
        Session = sessionmaker(bind=bind)
    elif 'config' in kargs:
        from sqlalchemy import create_engine
        bind = create_engine(kargs['config']['TORABOT_CONNECTION_STRING'])
        del kargs['config']
        Session = sessionmaker(bind=bind)
    elif 'make' in kargs:
        Session = kargs['make']
        del kargs['make']
    else:
        assert False, 'must provide engine, connection or config'

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


sessionguard = makesession


@contextmanager
def makeappsession(commit=False, **kargs):
    from flask import current_app
    kargs['config'] = current_app.config
    with makesession(commit=commit, **kargs) as session:
        yield session


def appsessionmaker():
    from flask import current_app
    bind = create_engine(current_app.config['TORABOT_CONNECTION_STRING'])
    return sessionmaker(bind=bind)
