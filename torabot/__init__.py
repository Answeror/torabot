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


def make(*args, **kargs):
    app = makeapp(*args, **kargs)

    from . import frontend
    frontend.make(app)

    #from .db.schema import create_all
    #from .core.session import makesession
    #with app.test_request_context():
        #with makesession(commit=True) as session:
            #create_all(session.connection())

    return app
