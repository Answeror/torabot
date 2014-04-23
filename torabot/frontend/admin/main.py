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
from ... import db
from . import bp
from .errors import AdminAuthError
from .auth import require_admin


log = Logger(__name__)


@bp.route('/queries', defaults={'page': 0}, methods=['GET'])
@bp.route('/queries/<int:page>', methods=['GET'])
@require_admin
def queries(page):
    room = current_app.config['TORABOT_PAGE_ROOM']
    with autoccontext(commit=False) as conn:
        queries = db.get_queries(
            conn,
            offset=page * room,
            limit=room,
        )
        total = db.get_query_count(conn)
    return render_template(
        'admin/queries.html',
        queries=queries,
        page=page,
        room=room,
        total=total,
        uri=lambda page: url_for('.queries', page=page),
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
        text = q[field]
        if isinstance(text, dict):
            text = json.dumps(text)
        return render_template(
            'jsoneditor.html',
            text=text,
            back=request.headers['referer'],
        )
    if request.method == 'POST':
        try:
            with autoccontext(commit=True) as conn:
                db.set_query_field_bi_id(conn, id, field, request.values['text'])
            return jsonify(dict(ok=True))
        except db.error.InvalidArgumentError:
            text = '无效值'
            return jsonify(dict(ok=False, message=dict(text=text, html=text))), 400


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
