def make(app):
    from . import main
    main.make(app)
    from . import admin
    admin.make(app)

    from ..core.mod import mod, mods
    from .momentjs import momentjs

    @app.context_processor
    def inject_locals():
        return dict(
            min=min,
            max=max,
            len=len,
            str=str,
            isinstance=isinstance,
            momentjs=momentjs,
            mod=mod,
            default_mod=app.config['TORABOT_DEFAULT_MOD'],
            mods=mods(),
        )
