from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


@contextmanager
def makesession(config, commit=False, **kargs):
    from sqlalchemy import create_engine
    engine = create_engine(config['TORABOT_CONNECTION_STRING'])
    Session = sessionmaker(bind=engine)
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
