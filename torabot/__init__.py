def make(*args, **kargs):
    from flask import Flask
    app = Flask(__name__)

    from . import view
    view.make(app)

    from .model import Session, Base

    if 'connection_string' in kargs:
        from sqlalchemy import create_engine
        engine = create_engine(kargs['connection_string'])
        bind = engine
    elif 'connection' in kargs:
        bind = kargs['connection']
    else:
        assert False, "must provide database connection or connection string"

    Base.metadata.create_all(bind)
    Session.configure(bind=bind)

    return app
