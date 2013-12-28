def make(*args, **kargs):
    from flask import Flask
    app = Flask(__name__)

    from . import view
    view.make(app)

    from .model import Session
    if 'connection_string' in kargs:
        from sqlalchemy import create_engine
        engine = create_engine(kargs['connection_string'])
        Session.configure(bind=engine)
    elif 'connection' in kargs:
        Session.configure(bind=kargs['connection'])
    else:
        assert False, "must provide database connection or connection string"

    return app
