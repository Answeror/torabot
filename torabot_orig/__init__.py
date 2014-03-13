def makeapp(*args, **kargs):
    from flask import Flask
    app = Flask(
        __name__,
        #template_folder='templates',
        #static_folder='static',
        **{name: kargs[name] for name in (
            'instance_path',
            'instance_relative_config',
        ) if name in kargs}
    )
    if 'config' in kargs:
        app.config.update(kargs['config'])
    return app


def initview(app, *args, **kargs):
    from . import view
    view.make(app)


def initdb(app, *args, **kargs):
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


def initopenid(app, *args, **kargs):
    from . import openid
    openid.make(app)


def make(*args, **kargs):
    app = makeapp(*args, **kargs)
    initview(app)
    initdb(app, *args, **kargs)
    initopenid(app)
    return app
