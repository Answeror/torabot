def make(*args, **kargs):
    from .app import App
    app = App(__name__, *args, **kargs)
    from .db import db
    db.init_app(app)
    from .core import core
    core.init_app(app)
    from .frontend import frontend
    frontend.init_app(app)
