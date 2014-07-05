from flask import jsonify, current_app
from .... import db
from ....celery import sync_all as task_sync_all
from ....core.mod import mods as _mods
from ....core.local import current_user, request_values
from ....core.connection import autoccontext
from ...admin.auth import admin_required
from .. import bp
from ..token import make_token
from ..auth import token_required
from ..errors import InvalidTokenError


@bp.route('/sync')
@token_required
def sync():
    task_sync_all.delay()
    return 'done'


@bp.route('/mods', methods=['GET'])
def mods():
    return jsonify(dict(result=[dict(
        name=m.name,
    ) for m in _mods()]))


@bp.route('/token', methods=['GET'])
@admin_required
def token():
    return jsonify({'result': make_token(current_user)})


@bp.route('/user/<int:id>/notices', methods=['GET'], defaults=dict(page=0))
@bp.route('/user/<int:id>/notices/<int:page>', methods=['GET'])
@token_required
def user_notices(id, page):
    room = current_app.config['TORABOT_NOTICE_ROOM']
    room = min(room, request_values.get('room', room))
    with autoccontext() as conn:
        notices = db.get_notices_bi_user_id(conn, user_id=id, page=page, room=room)
    return jsonify({'result': notices})


@bp.errorhandler(InvalidTokenError)
def invalid_token_error_guard(e):
    return jsonify({'error': {'message': 'invalid token'}}), 401
