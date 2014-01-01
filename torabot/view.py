import flask
from flask import (
    request,
    render_template,
)
from .query import query
from .model import Session, makesession, Subscription
from .kanji import translate
from logbook import Logger
from .sub import sub, unsub, has_sub
from . import auth


log = Logger(__name__)


def get_query_info():
    d = {}
    if 'query_id' in request.values:
        d['query_id'] = request.values['query_id']
    elif 'query_text' in request.values:
        d['query_text'] = request.values['query_text']
    else:
        raise Exception('neither query_id nor query_text provided')
    return d


def make(app):
    @app.route('/', methods=['GET'])
    def index():
        return render_template('layout.html')

    @app.route('/subs', methods=['GET'])
    @auth.require_session
    def subscriptions(user_id):
        with makesession() as session:
            return render_template(
                'subs.html',
                subs=(
                    session.query(Subscription)
                    .filter_by(user_id=user_id)
                    .all()
                )
            )

    @app.route('/search', methods=['GET'], defaults={'page': 0})
    @app.route('/search/<int:page>', methods=['GET'])
    def search(page):
        oq = request.args.get('q', '')
        tq = translate(oq)
        log.debug('query: {} -> {}', oq, tq)
        session = Session()
        try:
            arts = query(
                tq,
                page=page,
                room=app.config.get('TORABOT_PAGE_ROOM', 20),
                session=session
            )
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
    def subscribe():
        session = Session()
        try:
            sub(
                user_id=request.values['user_id'],
                session=session,
                **get_query_info()
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
    def unsubscribe():
        session = Session()
        try:
            unsub(
                user_id=request.values['user_id'],
                session=session,
                **get_query_info()
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
