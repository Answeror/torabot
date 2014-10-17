import os
import pkgutil
import importlib
from flask import Blueprint


bp = Blueprint('api', __name__)


for _, name, _ in pkgutil.iter_modules(
    [os.path.join(os.path.dirname(__file__), 'views')]
):
    importlib.import_module('.views.' + name, __name__)


def make(app):
    app.register_blueprint(bp, url_prefix='/api')
