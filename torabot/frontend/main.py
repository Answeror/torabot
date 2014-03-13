from flask import (
    request,
    render_template,
    current_app,
    session as flask_session
)
from logbook import Logger
from ..core.query import query
from ..core.watch import (
    watch,
    unwatch,
    watching,
    get_watches_bi_user_id
)
from ..core.notice import (
    get_notices_bi_user_id,
    get_pending_notices_bi_user_id
)
from ..core.kanji import translate
from ..core.session import makesession
from ..spider.tora import FrozenSpider
from . import auth, bp


log = Logger(__name__)


def get_query_info():
    d = {}
    if 'query_id' in request.values:
        d['query_id'] = request.values['query_id']
    #elif 'query_text' in request.values:
        #d['query_text'] = request.values['query_text']
    else:
        raise Exception('neither query_id nor query_text provided')
    return d


@bp.route('/', methods=['GET'])
def index():
    return render_template('layout.html')


@bp.route('/subs', methods=['GET'])
@auth.require_session
def subscriptions(user_id):
    with makesession() as session:
        return render_template(
            'subs.html',
            subs=get_watches_bi_user_id(session, user_id)
        )


@bp.route('/notice/all', methods=['GET'])
@auth.require_session
def all_notices(user_id):
    with makesession() as session:
        return render_template(
            'notices.html',
            tab='all',
            notices=get_notices_bi_user_id(session, user_id)
        )


@bp.route('/notice/pending', methods=['GET'])
@auth.require_session
def pending_notices(user_id):
    with makesession() as session:
        return render_template(
            'notices.html',
            tab='pending',
            notices=get_pending_notices_bi_user_id(session, user_id)
        )


@bp.route('/notice/conf', methods=['GET'])
@auth.require_session
def notice_conf(user_id):
    return render_template('noticeconf.html')


@bp.route('/search', methods=['GET'], defaults={'page': 0})
@bp.route('/search/<int:page>', methods=['GET'])
def search(page):
    oq = request.args.get('q', '')
    tq = translate(oq)
    log.debug('query: {} -> {}', oq, tq)
    with makesession() as session:
        room = current_app.config.get('TORABOT_PAGE_ROOM', 20)
        ret = query(
            tq,
            begin=room * page,
            end=room * (page + 1),
            return_detail=True,
            session=session,
            spider=FrozenSpider()
        )
        arts = ret.arts
        total = ret.total
        log.debug('query got {} arts', len(arts))
        session.commit()
        options = {}
        if 'userid' in flask_session:
            options['sub'] = watching(
                user_id=int(flask_session['userid']),
                query_id=ret.id,
                session=session,
            )
        ret = render_template(
            'list.html',
            arts=arts,
            query=tq,
            page=page,
            total=total,
            room=room,
            **options
        )
        session.commit()
        return ret


@bp.route('/sub', methods=['POST'])
def subscribe():
    with makesession() as session:
        try:
            watch(
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


@bp.route('/unsub', methods=['POST'])
def unsubscribe():
    with makesession() as session:
        try:
            unwatch(
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


@bp.context_processor
def inject_locals():
    return dict(
        min=min,
        max=max,
        len=len,
    )
