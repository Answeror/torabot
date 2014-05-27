from hashlib import md5
from functools import wraps
from nose.tools import assert_in
import json
from flask import (
    jsonify,
    request,
    current_app,
    render_template,
    redirect,
    url_for,
    make_response as flask_make_response
)
from flask.views import MethodView
from logbook import Logger
from ... import db
from ...core.query import query
from ...core.notice import (
    get_notices_bi_user_id,
    get_pending_notices_bi_user_id,
)
from ...core.watch import get_watches_bi_user_id
from ...core.connection import appccontext, autoccontext
from ...core.mod import mod
from ...core.local import is_user, current_user_id, request_values, current_user
from ...core.user import (
    update_email as core_update_email,
    add_email as core_add_email,
    activate_email as core_activate_email,
)
from ...cache import cache
from ..errors import AuthError
from . import bp
from .. import auth
from ..response import make_ok_response, make_response
from ..bulletin import get_bulletin_text, get_bulletin_type


log = Logger(__name__)


@bp.route('/', methods=['GET'])
def index():
    if is_user:
        return _watches(0, current_user.id)
    return render_template('index.html')


@bp.route('/intro', methods=['GET'])
def intro():
    resp = flask_make_response(render_template('index.html', intro=True))
    resp.set_cookie('intro', '1')
    return resp


def user_id_not_match(session_user_id):
    return int(request_values['user_id']) != session_user_id


def email_id_not_match(session_user_id):
    if 'email_id' not in request_values:
        return False
    with autoccontext() as conn:
        return db.get_email_bi_id(conn, request_values['email_id']).user_id != session_user_id


def check_request(session_user_id):
    if user_id_not_match(session_user_id) or email_id_not_match(session_user_id):
        raise AuthError('request user_id not equal to user_id in sessoin')


def request_checked(f):
    '''check user_id and email_id in request with user_id in session'''
    @wraps(f)
    def inner(*args, **kargs):
        assert_in('user_id', kargs)
        check_request(kargs['user_id'])
        return f(*args, **kargs)
    return inner


class RenameWatchView(MethodView):

    decorators = [request_checked, auth.require_session]

    def get(self, user_id):
        return render_template('rename_watch.html')

    def post(self, user_id):
        with appccontext(commit=True) as conn:
            db.rename_watch(
                conn,
                email_id=int(request_values['email_id']),
                query_id=int(request_values['query_id']),
                name=request_values['name'],
            )
        return make_response({
            'application/json': make_ok_response,
            'text/html': lambda: redirect(url_for('.watching'))
        })


rename_watch_view = RenameWatchView.as_view('rename_watch')
bp.add_url_rule('/watch/rename', view_func=rename_watch_view, methods=['GET'])
bp.add_url_rule('/watch/rename', view_func=rename_watch_view, methods=['POST'])


def _watches(page, user_id, snapshot=False):
    room = current_app.config['TORABOT_PAGE_ROOM']
    with appccontext() as conn:
        return render_template(
            'watches.html',
            page=page,
            room=room,
            total=db.get_watch_count_bi_user_id(conn, user_id),
            user=db.get_user_bi_id(conn, user_id),
            watches=get_watches_bi_user_id(
                conn,
                user_id,
                offset=page * room,
                limit=room
            ),
            uri=lambda page: url_for('.watching', page=page),
            snapshot=snapshot,
        )


@bp.route('/watches', methods=['GET'], defaults=dict(page=0))
@bp.route('/watches/<int:page>', methods=['GET'])
@auth.require_session
def watching(page, user_id):
    return _watches(page, user_id)


@bp.route('/example/watches', methods=['GET'])
def example_watching():
    return _watches(0, current_app.config['TORABOT_EXAMPLE_USER_ID'], True)


def _notices(tab, view, total, notices, page, user_id, snapshot=False):
    room = current_app.config['TORABOT_NOTICE_ROOM']
    with appccontext() as conn:
        return render_template(
            'notices.html',
            tab=tab,
            view=view,
            page=page,
            room=room,
            total=total(conn, user_id),
            notices=notices(conn, user_id, page=page, room=room),
            uri=lambda page: url_for("." + view, page=page),
            snapshot=snapshot,
        )


@bp.route('/notices', methods=['GET'], defaults=dict(page=0))
@bp.route('/notices/<int:page>', methods=['GET'])
@auth.require_session
def all_notices(page, user_id):
    return _notices(
        'all',
        all_notices.__name__,
        db.get_notice_count_bi_user_id,
        get_notices_bi_user_id,
        page,
        user_id,
    )


@bp.route('/example/notices', methods=['GET'])
def example_all_notices():
    return _notices(
        'all',
        example_all_notices.__name__,
        db.get_notice_count_bi_user_id,
        get_notices_bi_user_id,
        0,
        current_app.config['TORABOT_EXAMPLE_USER_ID'],
        True,
    )


@bp.route('/notices/pending', methods=['GET'], defaults=dict(page=0))
@bp.route('/notices/pending/<int:page>', methods=['GET'])
@auth.require_session
def pending_notices(page, user_id):
    return _notices(
        'pending',
        pending_notices.__name__,
        db.get_pending_notice_count_bi_user_id,
        get_pending_notices_bi_user_id,
        page,
        user_id
    )


@bp.route('/notice/config', methods=['GET', 'POST', 'PATCH'])
@auth.require_session
def notice_conf(user_id):
    if request.method == 'GET':
        with appccontext() as conn:
            return render_template(
                'noticeconf.html',
                user=db.get_user_detail_bi_id(conn, user_id)
            )

    if request.method == 'POST':
        if 'id' in request.values:
            return {
                'update': update_email,
                'delete': delete_email,
                'activate': activate_email,
            }[request.values['action']](user_id)
        return add_email(user_id)


def activate_email(user_id):
    core_activate_email(int(request.values['id']))
    return render_template(
        'message.html',
        ok=True,
        message='激活邮件已发送至 %s , 请根据邮件中的提示完成激活.' % request.values['text']
    )


def add_email(user_id):
    email = request.values['text']
    core_add_email(
        user_id=user_id,
        email=email,
        label=request.values['label'],
    )
    return render_template(
        'message.html',
        ok=True,
        message='邮箱添加. 激活邮件已发送至 %s , 请根据邮件中的提示完成添加.' % email
    )


def delete_email(user_id):
    with appccontext(commit=True) as conn:
        db.del_email_bi_id(
            conn,
            id=request.values['id'],
        )
    return redirect(url_for('.notice_conf'))


def update_email(user_id):
    email = request.values['text']
    if core_update_email(
        user_id=user_id,
        email_id=int(request.values['id']),
        email=email,
        label=request.values['label'],
    ):
        return render_template(
            'message.html',
            ok=True,
            message='邮箱已更改, 需要重新激活. 激活邮件已发送至 %s , 请根据邮件中的提示完成更改.' % email
        )

    return redirect(url_for('.notice_conf'))


@cache.memoize(timeout=600)
def _advanced_search(kind, values, snapshot):
    return render_template(
        'advanced_search.html',
        query_kind=kind,
        content=mod(kind).format_advanced_search('web', **values),
        snapshot=snapshot,
    )


@bp.route('/search/advanced/<kind>', methods=['GET'])
def advanced_search(kind):
    return _advanced_search(kind, dict(request.values.items()), snapshot=False)


@bp.route('/example/search/advanced/<kind>', methods=['GET'])
def example_advanced_search(kind):
    return _advanced_search(kind, dict(request.values.items()), snapshot=True)


def get_standard_query():
    text = request.values.get('q', '').strip()
    try:
        d = json.loads(text)
        if not isinstance(d, dict):
            raise Exception('query not standard')
    except:
        d = dict(request.values.items())

    if not d:
        return ''
    if 'q' in d and len(d) == 1:
        return d['q']
    return json.dumps(d, sort_keys=True)


@bp.route('/search/<kind>', methods=['GET'])
def search(kind):
    return _search(kind, snapshot=False)


@bp.route('/example/search/<kind>', methods=['GET'])
def example_search(kind):
    return _search(kind, snapshot=True)


def _search(kind, snapshot):
    text = get_standard_query()
    log.info('search: %r' % text)
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
            options['watching'] = db.watching(
                conn,
                user_id=current_user_id._get_current_object(),
                query_id=q.id
            )
            options['states'] = db.get_email_watch_states(
                conn,
                user_id=current_user_id._get_current_object(),
                query_id=q.id
            )
    return render_template('list.html', snapshot=snapshot, **options)


@bp.route('/watch/add', methods=['POST'])
@auth.require_session
@request_checked
def watch(user_id):
    query_id = int(request_values['query_id'])
    email_id = int(request_values['email_id'])

    options = {}
    if 'name' in request_values:
        options.update(name=request_values['name'])

    with appccontext(commit=True) as conn:
        db.watch(conn, email_id=email_id, query_id=query_id, **options)

    return make_response({
        'application/json': make_ok_response,
        'text/html': lambda: redirect(url_for(
            '.rename_watch',
            user_id=user_id,
            email_id=email_id,
            query_id=query_id
        )),
    })


@bp.route('/watch/del', methods=['POST'])
@auth.require_session
@request_checked
def unwatch(user_id):
    query_id = int(request_values['query_id'])
    email_id = int(request_values['email_id'])

    with appccontext(commit=True) as conn:
        db.unwatch(conn, email_id=email_id, query_id=query_id)

    return make_response({
        'application/json': make_ok_response,
        'text/html': lambda: redirect(url_for('.watching')),
    })


@bp.route('/about')
def about():
    return render_template('about.html')


@bp.route('/faq')
def faq():
    return render_template('faq.html')


@bp.route('/help/<name>')
def help(name):
    return render_template(
        'help.html',
        query_kind=name,
        content=mod(name).format_help_page()
    )


@bp.route('/completion-options/<kind>')
def completion_options(kind):
    return jsonify(dict(result=mod(kind).completion_options))


@bp.context_processor
def inject_locals():
    return dict(
        bulletin_text=get_bulletin_text(),
        bulletin_type=get_bulletin_type(),
        bulletin_id=md5((get_bulletin_text() or '').encode('utf-8')).hexdigest()
    )
