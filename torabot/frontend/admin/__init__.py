from flask import Blueprint


bp = Blueprint(
    'admin',
    __name__,
    static_folder='static',
    template_folder='templates',
    static_url_path='/admin/static',
    url_prefix='/admin'
)


from .main import *


def make(app):
    app.register_blueprint(bp)
