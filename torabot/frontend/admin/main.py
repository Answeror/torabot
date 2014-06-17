import json
import mimeparse
from logbook import Logger
from flask import (
    render_template,
    request,
    current_app,
    url_for,
    jsonify,
)
from ...core.connection import autoccontext
from ...core.version import get_version
from ... import db
from ..response import make_ok_response
from ..bulletin import (
    get_bulletin_text,
    set_bulletin_text,
    get_bulletin_type,
    set_bulletin_type,
)
from . import bp
from .errors import AdminAuthError
from .auth import require_admin


log = Logger(__name__)


def page_room():
    return current_app.config['TORABOT_PAGE_ROOM']


@bp.route('/queries', defaults={'page': 0}, methods=['GET'])
@bp.route('/queries/<int:page>', methods=['GET'])
@require_admin
def queries(page):
    with autoccontext(commit=False) as conn:
        return render_template(
            'admin/queries.html',
            queries=db.get_queries(
                conn,
                offset=page * page_room(),
                limit=page_room(),
            ),
            total=db.get_query_count(conn),
            page=page,
            room=page_room(),
            uri=lambda page: url_for('.queries', page=page),
        )


@bp.route('/users', defaults={'page': 0}, methods=['GET'])
@bp.route('/users/<int:page>', methods=['GET'])
@require_admin
def users(page):
    with autoccontext(commit=False) as conn:
        return render_template(
            'admin/users.html',
            users=db.get_users_detail(
                conn,
                offset=page * page_room(),
                limit=page_room(),
                order_by='id',
                desc=True,
            ),
            total=db.get_user_count(conn),
            page=page,
            room=page_room(),
            uri=lambda page: url_for('.users', page=page),
        )


@bp.route('/queries/active', defaults={'page': 0}, methods=['GET'])
@bp.route('/queries/active/<int:page>', methods=['GET'])
@require_admin
def active_queries(page):
    room = current_app.config['TORABOT_PAGE_ROOM']
    with autoccontext(commit=False) as conn:
        queries = db.get_active_queries(
            conn,
            offset=page * room,
            limit=room,
        )
        total = db.get_active_query_count(conn)
    return render_template(
        'admin/queries.html',
        queries=queries,
        page=page,
        room=room,
        total=total,
        uri=lambda page: url_for('.active_queries', page=page),
    )


@bp.route('/query/<id>/<field>', methods=['GET', 'POST'])
@require_admin
def query(id, field):
    if request.method == 'GET':
        with autoccontext(commit=False) as conn:
            q = db.get_query_bi_id(conn, id)
        value = q[field]
        if isinstance(value, dict):
            value = json.dumps(value)
        return render_template(
            'jsoneditor.html',
            value=value,
            back=request.headers['referer'],
        )
    if request.method == 'POST':
        with autoccontext(commit=True) as conn:
            db.set_query_field_bi_id(conn, id, field, request.json['value'])
        return make_ok_response()


@bp.route('/user/<id>/<field>', methods=['POST'])
@require_admin
def user(id, field):
    if request.method == 'POST':
        with autoccontext(commit=True) as conn:
            db.set_user_field_bi_id(conn, id, field, request.json['value'])
        return make_ok_response()


@bp.route('/', methods=['GET'])
@bp.route('/dashboard', methods=['GET'])
@require_admin
def dashboard():
    with autoccontext(commit=True) as conn:
        return render_template('admin/dashboard.html', stats=[
            ('版本', get_version()),
            ('用户', db.get_user_count(conn)),
            ('活跃查询', db.get_active_query_count(conn)),
        ])


@bp.route('/bulletin', methods=['GET', 'POST'])
@require_admin
def bulletin():
    if request.method == 'GET':
        return render_template(
            'admin/bulletin.html',
            text=get_bulletin_text(),
            type=get_bulletin_type(),
        )
    if request.method == 'POST':
        log.info(request.json['type'])
        set_bulletin_text(request.json['text'])
        set_bulletin_type(request.json['type'])
        return make_ok_response()


@bp.errorhandler(AdminAuthError)
def admin_auth_error_guard(e):
    text = '管理员认证错误'

    def format_json():
        return jsonify(dict(message=dict(text=text, html=text)))

    def format_html():
        return render_template(
            'message.html',
            ok=False,
            message=text
        )

    formats = {
        'application/json': format_json,
        'text/html': format_html,
    }
    return formats[mimeparse.best_match(formats, request.headers['accept'])](), 401
