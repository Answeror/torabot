from flask import Blueprint


bp = Blueprint('m', __name__)


from . import main
assert main


def make(app):
    app.register_blueprint(bp, url_prefix='/m')
