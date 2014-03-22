from flask import Blueprint


bp = Blueprint(
    'ui',
    __name__,
    static_folder='static',
    template_folder='templates',
    static_url_path='/ui/static'
)


from .main import *
from .thumbnail import *
from .openid import *


def make(app):
    app.register_blueprint(bp)
    oid.init_app(app)
