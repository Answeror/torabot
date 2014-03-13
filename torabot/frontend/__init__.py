from flask import Blueprint


bp = Blueprint('ui', __name__, template_folder='templates')


from .main import *
from .openid import *


def make(app):
    app.register_blueprint(bp)
    oid.init_app(app)
