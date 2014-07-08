from flask import jsonify, current_app
from .... import db
from .... import celery
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
    celery.sync_all.delay()
    return 'done'


@bp.route('/log-to-file')
@token_required
def log_to_file():
    celery.log_to_file.delay()
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


@bp.route('/delete-old-changes')
@token_required
def delete_old_changes():
    return jsonify({
        'result': {
            "deleted": celery.del_old_changes.apply_async().get()
        }
    })


@bp.route('/delete-inactive-queries')
@token_required
def delete_inactive_queries():
    return jsonify({
        'result': {
            "deleted": celery.del_inactive_queries.apply_async().get()
        }
    })


@bp.errorhandler(InvalidTokenError)
def invalid_token_error_guard(e):
    return jsonify({'error': {'message': 'invalid token'}}), 401
