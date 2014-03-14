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

    from . import api
    api.make(app)

    return app
