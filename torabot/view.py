from flask import (
    request,
    render_template,
)
from .query import query
from .model import Session


def make(app):
    @app.route('/', methods=['GET'])
    def index():
        q = request.args.get('q', '')
        session = Session()
        try:
            ret = render_template('list.html', arts=query(q, session=session))
            session.commit()
            session.close()
            return ret
        except:
            session.rollback()
            raise
