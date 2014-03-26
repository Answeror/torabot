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


def make(*args, **kargs):
    app = makeapp(*args, **kargs)

    from . import frontend
    frontend.make(app)

    from . import api
    api.make(app)

    from .core.mod import mods
    import jinja2
    with app.app_context():
        app.jinja_loader = jinja2.ChoiceLoader([
            app.jinja_loader,
            jinja2.FileSystemLoader([mod.template_folder for mod in mods() if mod.template_folder])
        ])

    return app
