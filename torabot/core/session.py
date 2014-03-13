from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from flask import current_app


@contextmanager
def makesession(commit=False, **kargs):
    from sqlalchemy import create_engine
    engine = create_engine(current_app.config['TORABOT_CONNECTION_STRING'])
    Session = sessionmaker(bind=engine)
    session = Session(**kargs)
    try:
        yield session
        if commit:
            session.commit()
    except:
        session.rollback()
        raise
