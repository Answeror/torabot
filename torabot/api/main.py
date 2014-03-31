from flask import jsonify
from . import bp
from ..celery import sync_all as task_sync_all
from ..core.mod import mods as _mods


@bp.route('/sync')
def sync():
    task_sync_all.delay()
    return 'done'


@bp.route('/mods')
def mods():
    return jsonify(dict(result=[dict(
        name=m.name,
    ) for m in _mods()]))
