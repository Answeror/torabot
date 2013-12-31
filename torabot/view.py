import flask
from flask import (
    request,
    render_template,
)
from .query import query
from .model import Session
from .kanji import translate
from logbook import Logger
from .sub import sub, unsub, has_sub


log = Logger(__name__)


def make(app):
    @app.route('/', methods=['GET'])
    def index():
        return render_template('layout.html')

    @app.route('/search', methods=['GET'])
    def search():
        oq = request.args.get('q', '')
        tq = translate(oq)
        log.debug('query: {} -> {}', oq, tq)
        session = Session()
        try:
            arts = query(tq, session=session)
            session.commit()
            options = {}
            if 'userid' in flask.session:
                options['sub'] = has_sub(
                    user_id=int(flask.session['userid']),
                    query_text=tq,
                    session=session,
                )
            ret = render_template(
                'list.html',
                arts=arts,
                query=tq,
                **options
            )
            session.commit()
            session.close()
            return ret
        except:
            session.rollback()
            raise

    @app.route('/sub', methods=['POST'])
    def subsribe():
        session = Session()
        try:
            sub(
                user_id=request.values['userid'],
                query_text=request.values['query'],
                session=session,
            )
            session.commit()
            session.close()
            return render_template(
                'message.html',
                ok=True,
                message='subscribe done'
            )
        except:
            log.exception('sub failed')
            session.rollback()
            return render_template(
                'message.html',
                ok=False,
                message='subscribe failed'
            )

    @app.route('/unsub', methods=['POST'])
    def unsubsribe():
        session = Session()
        try:
            unsub(
                user_id=request.values['userid'],
                query_text=request.values['query'],
                session=session,
            )
            session.commit()
            session.close()
            return render_template(
                'message.html',
                ok=True,
                message='unsubscribe done'
            )
        except:
            log.exception('sub failed')
            session.rollback()
            return render_template(
                'message.html',
                ok=False,
                message='unsubscribe failed'
            )
