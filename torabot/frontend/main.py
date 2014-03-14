from nose.tools import assert_equal
from flask import (
    request,
    render_template,
    current_app,
    session as flask_session
)
from logbook import Logger
from ..core.query import query
from ..db import (
    watch as _watch,
    unwatch as _unwatch,
    watching as _watching,
    get_sorted_watch_details_bi_user_id,
    get_user_bi_id,
    set_email,
)
from ..core.notice import (
    get_notices_bi_user_id,
    get_pending_notices_bi_user_id,
)
from ..core.kanji import translate
from ..spider.tora import FrozenSpider
from . import auth, bp
from ..ut.session import makeappsession as makesession


log = Logger(__name__)


@bp.route('/', methods=['GET'])
def index():
    return render_template('layout.html')


@bp.route('/watching', methods=['GET'])
@auth.require_session
def watching(user_id):
    with makesession() as session:
        return render_template(
            'watching.html',
            user=get_user_bi_id(session.connection(), user_id),
            watches=get_sorted_watch_details_bi_user_id(
                session.connection(),
                user_id
            )
        )


@bp.route('/notice/all', methods=['GET'])
@auth.require_session
def all_notices(user_id):
    with makesession() as session:
        return render_template(
            'notices.html',
            tab='all',
            notices=get_notices_bi_user_id(session.connection(), user_id)
        )


@bp.route('/notice/pending', methods=['GET'])
@auth.require_session
def pending_notices(user_id):
    with makesession() as session:
        return render_template(
            'notices.html',
            tab='pending',
            notices=get_pending_notices_bi_user_id(session.connection(), user_id)
        )


@bp.route('/notice/config', methods=['GET', 'POST'])
@auth.require_session
def notice_conf(user_id):
    if request.method == 'GET':
        with makesession() as session:
            return render_template(
                'noticeconf.html',
                user=get_user_bi_id(session.connection(), user_id)
            )

    assert_equal(request.method, 'POST')
    try:
        with makesession(commit=True) as session:
            set_email(
                session.connection(),
                id=user_id,
                email=request.values['email'],
            )
        return render_template(
            'message.html',
            ok=True,
            message='更新成功'
        )
    except:
        log.exception(
            'user {} change email to {} failed',
            user_id,
            request.values['email']
        )
        return render_template(
            'message.html',
            ok=True,
            message='更新失败'
        )


@bp.route('/search', methods=['GET'], defaults={'page': 0})
@bp.route('/search/<int:page>', methods=['GET'])
def search(page):
    oq = request.args.get('q', '')
    tq = translate(oq)
    log.debug('query: {} -> {}', oq, tq)
    with makesession(commit=True) as session:
        room = current_app.config.get('TORABOT_PAGE_ROOM', 20)
        q = query(
            tq,
            begin=room * page,
            end=room * (page + 1),
            return_detail=True,
            conn=session.connection(),
            spider=FrozenSpider()
        )
        session.commit()
        options = {}
        if 'userid' in flask_session:
            options['watching'] = _watching(
                session.connection(),
                user_id=int(flask_session['userid']),
                query_id=q.id,
            )
        return render_template(
            'list.html',
            query=q,
            page=page,
            room=room,
            **options
        )


@bp.route('/watch', methods=['POST'])
def watch():
    with makesession() as session:
        try:
            _watch(
                session.connection(),
                user_id=request.values['user_id'],
                query_id=request.values['query_id'],
            )
            session.commit()
            session.close()
            return render_template(
                'message.html',
                ok=True,
                message='订阅成功'
            )
        except:
            log.exception('watch failed')
            session.rollback()
            return render_template(
                'message.html',
                ok=False,
                message='订阅失败'
            )


@bp.route('/unwatch', methods=['POST'])
def unwatch():
    with makesession() as session:
        try:
            _unwatch(
                session.connection(),
                user_id=request.values['user_id'],
                query_id=request.values['query_id'],
            )
            session.commit()
            session.close()
            return render_template(
                'message.html',
                ok=True,
                message='取消订阅成功'
            )
        except:
            log.exception('unwatch failed')
            session.rollback()
            return render_template(
                'message.html',
                ok=False,
                message='取消订阅失败'
            )


@bp.context_processor
def inject_locals():
    return dict(
        min=min,
        max=max,
        len=len,
    )
