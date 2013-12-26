from flask import (
    request,
    render_template,
)
from .spider import fetch_and_parse_all


def make(app):
    @app.route('/', methods=['GET'])
    def index():
        q = request.args.get('q', '')
        return render_template('list.html', arts=fetch_and_parse_all(q))
