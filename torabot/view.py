from flask import (
    request,
    render_template,
)
from .query import query
from .model import Session
from .kanji import translate
from logbook import Logger


log = Logger(__name__)


def make(app):
    @app.route('/', methods=['GET'])
    def index():
        oq = request.args.get('q', '')
        q = translate(oq)
        log.debug('query: {} -> {}', oq, q)
        session = Session()
        try:
            ret = render_template('list.html', arts=query(q, session=session))
            session.commit()
            session.close()
            return ret
        except:
            session.rollback()
            raise
