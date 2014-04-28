import json
from nose.tools import assert_equal
from flask import (
    request,
    current_app,
    render_template,
    redirect,
    url_for,
)
from logbook import Logger
from ...core.query import query
from ...db import (
    watch as _watch,
    unwatch as _unwatch,
    watching as _watching,
    rename_watch as _rename_watch,
    get_user_bi_id,
    set_email,
    get_notice_count_bi_user_id,
    get_pending_notice_count_bi_user_id,
)
from ...core.notice import (
    get_notices_bi_user_id,
    get_pending_notices_bi_user_id,
)
from ...core.watch import get_watches_bi_user_id
from ...core.connection import appccontext
from ...core.mod import mod
from ...core.local import is_user, current_user_id
from ...cache import cache
from ..errors import AuthError
from . import bp
from .. import auth


log = Logger(__name__)


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


def message(text, ok=True):
    return render_template('message.html', ok=ok, message=text)


def done(text):
    return message(text, True)


def failed(text):
    return message(text, False)


def check_request_user_id(session_user_id):
    if int(request.values['user_id']) != session_user_id:
        raise AuthError('request user_id not equal to user_id in sessoin')


@bp.route('/watch/rename', methods=['GET', 'POST'])
@auth.require_session
def rename_watch(user_id):
    check_request_user_id(user_id)
    if request.method == 'GET':
        return render_template('rename_watch.html')
    else:
        try:
            with appccontext(commit=True) as conn:
                _rename_watch(
                    conn,
                    user_id=int(request.values['user_id']),
                    query_id=int(request.values['query_id']),
                    name=request.values['name'],
                )
            return redirect(url_for('.watching'))
        except:
            log.exception('watch failed')
            return failed('重命名失败')


@bp.route('/watch', methods=['GET'])
@auth.require_session
def watching(user_id):
    with appccontext() as conn:
        return render_template(
            'watching.html',
            user=get_user_bi_id(conn, user_id),
            watches=get_watches_bi_user_id(conn, user_id)
        )


@bp.route('/notice/all', methods=['GET'], defaults=dict(page=0))
@bp.route('/notice/all/<int:page>', methods=['GET'])
@auth.require_session
def all_notices(page, user_id):
    room = current_app.config['TORABOT_NOTICE_ROOM']
    with appccontext() as conn:
        return render_template(
            'notices.html',
            tab='all',
            view=all_notices.__name__,
            page=page,
            room=room,
            total=get_notice_count_bi_user_id(conn, user_id),
            notices=get_notices_bi_user_id(conn, user_id, page=page, room=room)
        )


@bp.route('/notice/pending', methods=['GET'], defaults=dict(page=0))
@bp.route('/notice/pending/<int:page>', methods=['GET'])
@auth.require_session
def pending_notices(page, user_id):
    room = current_app.config['TORABOT_NOTICE_ROOM']
    with appccontext() as conn:
        return render_template(
            'notices.html',
            tab='pending',
            view=pending_notices.__name__,
            page=page,
            room=room,
            total=get_pending_notice_count_bi_user_id(conn, user_id),
            notices=get_pending_notices_bi_user_id(conn, user_id, page=page, room=room)
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
            ok=False,
            message='更新失败'
        )


@cache.memoize(timeout=600)
def _advanced_search(kind, values):
    return render_template(
        'advanced_search.html',
        query_kind=kind,
        content=mod(kind).format_advanced_search('web', **values)
    )


@bp.route('/search/advanced/<kind>', methods=['GET'])
def advanced_search(kind):
    return _advanced_search(kind, dict(request.values.items()))


def get_standard_query():
    text = request.values.get('q', '').strip()
    try:
        d = json.loads(text)
    except:
        d = dict(request.values.items())

    if not d:
        return ''
    if 'q' in d and len(d) == 1:
        return d['q']
    return json.dumps(d, sort_keys=True)


@bp.route('/search/<kind>', methods=['GET'])
def search(kind):
    text = get_standard_query()
    with appccontext(commit=True) as conn:
        q = query(
            conn=conn,
            kind=kind,
            text=text,
            timeout=current_app.config['TORABOT_SPY_TIMEOUT'],
        )
        options = dict(
            query=q,
            content=mod(q.kind).format_query_result('web', q)
        )
        if is_user:
            options['watching'] = _watching(
                conn,
                user_id=current_user_id._get_current_object(),
                query_id=q.id,
            )
    return render_template('list.html', **options)


@bp.route('/watch/add', methods=['POST'])
@auth.require_session
def watch(user_id):
    check_request_user_id(user_id)
    try:
        query_id = int(request.values['query_id'])
        with appccontext(commit=True) as conn:
            _watch(conn, user_id=user_id, query_id=query_id)
        return redirect(url_for(
            '.rename_watch',
            user_id=user_id,
            query_id=query_id
        ))
    except:
        log.exception('watch failed')
        return failed('订阅失败')


@bp.route('/watch/del', methods=['POST'])
@auth.require_session
def unwatch(user_id):
    check_request_user_id(user_id)
    try:
        query_id = int(request.values['query_id'])
        with appccontext(commit=True) as conn:
            _unwatch(conn, user_id=user_id, query_id=query_id)
        return redirect(url_for('.watching'))
    except:
        log.exception('unwatch failed')
        return failed('退订失败')


@bp.route('/about')
def about():
    return render_template('about.html')


@bp.route('/help/<name>')
def help(name):
    return render_template(
        'help.html',
        query_kind=name,
        content=mod(name).format_help_page()
    )
