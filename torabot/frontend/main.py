from nose.tools import assert_equal
from flask import (
    request,
    current_app,
    render_template,
    session as flask_session
)
from logbook import Logger
from ..core.query import query
from ..db import (
    watch as _watch,
    unwatch as _unwatch,
    watching as _watching,
    get_user_bi_id,
    set_email,
)
from ..core.notice import (
    get_notices_bi_user_id,
    get_pending_notices_bi_user_id,
)
from ..core.watch import get_watches_bi_user_id
from ..core.kanji import translate
from . import auth, bp
from ..ut.connection import appccontext
from ..core.mod import mod
from .momentjs import momentjs


log = Logger(__name__)


@bp.route('/', methods=['GET'])
def index():
    return render_template('layout.html')


@bp.route('/watching', methods=['GET'])
@auth.require_session
def watching(user_id):
    with appccontext() as conn:
        return render_template(
            'watching.html',
            user=get_user_bi_id(conn, user_id),
            watches=get_watches_bi_user_id(conn, user_id)
        )


@bp.route('/notice/all', methods=['GET'])
@auth.require_session
def all_notices(user_id):
    with appccontext() as conn:
        return render_template(
            'notices.html',
            tab='all',
            notices=get_notices_bi_user_id(conn, user_id)
        )


@bp.route('/notice/pending', methods=['GET'])
@auth.require_session
def pending_notices(user_id):
    with appccontext() as conn:
        return render_template(
            'notices.html',
            tab='pending',
            notices=get_pending_notices_bi_user_id(conn, user_id)
        )


@bp.route('/notice/config', methods=['GET', 'POST'])
@auth.require_session
def notice_conf(user_id):
    if request.method == 'GET':
        with appccontext() as conn:
            return render_template(
                'noticeconf.html',
                user=get_user_bi_id(conn, user_id)
            )

    assert_equal(request.method, 'POST')
    try:
        with appccontext(commit=True) as conn:
            set_email(
                conn,
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
    query_text = translate(request.args.get('q', ''))
    with appccontext(commit=True) as conn:
        q = query(
            conn=conn,
            kind='tora',
            text=query_text,
            timeout=current_app.config['TORABOT_SPY_TIMEOUT'],
            slaves=current_app.config['TORABOT_SPY_SLAVES'],
        )
        options = dict(
            query=q,
            content=mod(q.kind).views.web.format_query_result(q.result)
        )
        if 'userid' in flask_session:
            options['watching'] = _watching(
                conn,
                user_id=int(flask_session['userid']),
                query_id=q.id,
            )
    return render_template('list.html', **options)


@bp.route('/watch', methods=['POST'])
def watch():
    try:
        with appccontext(commit=True) as conn:
            _watch(
                conn,
                user_id=request.values['user_id'],
                query_id=request.values['query_id'],
            )
        return render_template(
            'message.html',
            ok=True,
            message='订阅成功'
        )
    except:
        log.exception('watch failed')
        return render_template(
            'message.html',
            ok=False,
            message='订阅失败'
        )


@bp.route('/unwatch', methods=['POST'])
def unwatch():
    try:
        with appccontext(commit=True) as conn:
            _unwatch(
                conn,
                user_id=request.values['user_id'],
                query_id=request.values['query_id'],
            )
            return render_template(
                'message.html',
                ok=True,
                message='退订成功'
            )
    except:
        log.exception('unwatch failed')
        return render_template(
            'message.html',
            ok=False,
            message='退订失败'
        )


@bp.context_processor
def inject_locals():
    return dict(
        min=min,
        max=max,
        len=len,
        momentjs=momentjs,
    )
