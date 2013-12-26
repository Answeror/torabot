def make(*args, **kargs):
    from flask import Flask
    app = Flask(__name__)
    from . import view
    view.make(app)
    return app
