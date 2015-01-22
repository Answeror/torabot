import os
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
    session,
    make_response as flask_make_response
)
from flask.views import MethodView
from logbook import Logger
from ...core import core
from ..errors import AuthError, BusyError
from ..response import make_ok_response, make_response
from ..bulletin import get_bulletin_text, get_bulletin_type
from .. import auth
from . import bp


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


def _advanced_search(kind, values, snapshot):
    if mod(kind).public or is_user:
        return render_template(
            'advanced_search.html',
            query_kind=kind,
            content=mod(kind).format_advanced_search('web', **values),
            snapshot=snapshot,
        )
    return redirect(url_for(".index"))


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
    try:
        if mod(kind).public or is_user or current_app.config['TORABOT_DEBUG']:
            return __search(kind, snapshot)
    except:
        log.debug('search %s for %r failed' % (kind, get_standard_query()))
        raise
    return redirect(url_for(".index"))


def __search(kind, snapshot):
    text = get_standard_query()
    log.info('search: %r' % text)
    with appccontext(commit=True) as conn:
        q = query(
            kind=kind,
            text=text,
            timeout=current_app.config['TORABOT_SPY_TIMEOUT'],
            backend=PostgreSQL(conn=conn),
        )
        if q is None:
            raise BusyError()
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


@bp.route('/help/<kind>')
def help(kind):
    if mod(kind).public or is_user:
        return render_template(
            'help.html',
            query_kind=kind,
            content=mod(kind).format_help_page()
        )
    return redirect(url_for(".index"))


@bp.route('/completion-options/<kind>')
def completion_options(kind):
    return jsonify(dict(result=mod(kind).completion_options))


@bp.route('/call/<kind>')
def call(kind):
    if request.method == 'GET':
        return jsonify(dict(result=mod(kind).get(
            json.loads(request.args['arg'])
        )))
    raise Exception('only support get now')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        if verity_password_bi_email(
            request.form.get('email'),
            request.form.get('password')
        ):
            session['user_id'] = get_user_id_bi_email(request.form['email'])
            return redirect(url_for('.index'))
        else:
            return render_template(
                'login.html',
                ok=False,
                message='该邮箱尚未注册或密码错误'
            )


@bp.route('/reset', methods=['GET', 'POST'], defaults={'payload': None})
@bp.route('/reset/<payload>', methods=['GET', 'POST'])
def reset_password(payload):
    if payload is None:
        if request.method == 'GET':
            return render_template('reset_password.html')
        else:
            if not has_email(request.form.get('email')):
                return render_template(
                    'reset_password.html',
                    ok=False,
                    message='该邮箱尚未注册'
                )
            send_password_reset_email(request.form['email'])
            return render_template(
                'message.html',
                ok=True,
                message='密码重置邮件已发送至 %s , 请根据邮件中的提示完成重置.' % request.form['email']
            )
    else:
        email = get_password_reset_email(payload)
        if not email:
            return render_template(
                'message.html',
                ok=False,
                message='密码重置链接已失效.'
            )

        if request.method == 'GET':
            return render_template('set_password.html', email=email)
        else:
            if request.form.get('email') != email:
                return redirect(url_for('.index'))
            if (
                not request.form.get('password') or
                request.form.get('password') != request.form.get('confirm')
            ):
                return render_template(
                    'set_password.html',
                    email=email,
                    ok=False,
                    message='请正确输入两遍密码'
                )
            set_password_bi_email(email, request.form['password'])
            return redirect(url_for('.login'))


@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('.index'))


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        if not request.form.get('name', '').strip():
            return render_template(
                'signup.html',
                ok=False,
                message='昵称不能为空'
            )
        if not request.form.get('email', '').strip():
            return render_template(
                'signup.html',
                ok=False,
                message='邮箱不能为空'
            )
        if (
            not request.form.get('password') or
            request.form.get('password') != request.form.get('confirm')
        ):
            return render_template(
                'signup.html',
                ok=False,
                message='请正确输入两遍密码'
            )
        try:
            user = add_user(
                request.form['name'].strip(),
                request.form['email'].strip(),
                request.form['password'],
                next_uri=url_for('.index')
            )
        except DuplicateUsernameError:
            return render_template(
                'signup.html',
                ok=False,
                message='该昵称已被使用'
            )
        except DuplicateEmailError:
            return render_template(
                'signup.html',
                ok=False,
                message='该邮箱已被使用'
            )
        session['user_id'] = user.id
        return redirect(url_for('.index'))


@bp.route('/activate/<payload>')
def activate_user(payload):
    next_uri = activate_user_and_get_next_uri(payload)
    if not next_uri:
        return render_template(
            'message.html',
            ok=False,
            message='激活链接已失效.'
        )

    return redirect(next_uri)


@bp.context_processor
def inject_locals():
    return dict(
        bulletin_text=get_bulletin_text(),
        bulletin_type=get_bulletin_type(),
        bulletin_id=md5((get_bulletin_text() or '').encode('utf-8')).hexdigest()
    )


@bp.url_defaults
def add_hash_for_static_files(endpoint, values):
    if not endpoint or endpoint.split('.')[-1] != 'static':
        return
    filename = values['filename']
    redis_key = 'torabot:temp:static:' + filename
    values['v'] = redis.get(redis_key)
    if values['v']:
        return
    filepath = os.path.join(bp.static_folder, filename)
    if os.path.isfile(filepath):
        with open(filepath, 'rb') as static_file:
            filehash = md5(static_file.read()).hexdigest()
            values['v'] = filehash
            redis.set(redis_key, filehash)
