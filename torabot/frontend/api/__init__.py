from flask import Blueprint


bp = Blueprint('api', __name__)


from . import main
assert main


def make(app):
    app.register_blueprint(bp, url_prefix='/api')
