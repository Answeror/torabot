from flask import Blueprint


name = 'booru'
bp = Blueprint(
    name,
    __name__,
    static_folder='static',
    template_folder='templates',
    static_url_path='/%s/static' % name
)
