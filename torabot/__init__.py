def makeapp(*args, **kargs):
    from flask import Flask
    app = Flask(
        __name__,
        **{name: kargs[name] for name in (
            'instance_path',
            'instance_relative_config',
        ) if name in kargs}
    )

    try:
        import toraconf
        app.config.from_object(toraconf)
    except:
        from . import conf
        app.config_from_object(conf)

    if 'config' in kargs:
        app.config.update(kargs['config'])
    return app


def makeparts(app):
    from . import frontend
    from . import api
    from .core import mod

    for part in [frontend, api, mod]:
        part.make(app)


def make(*args, **kargs):
    app = makeapp(*args, **kargs)
    makeparts(app)
    return app
