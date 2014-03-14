from flask import current_app
from . import bp
from ..task.sync import sync_all as task_sync_all


@bp.route('/sync')
def sync():
    task_sync_all(current_app.config)
    return 'done'
