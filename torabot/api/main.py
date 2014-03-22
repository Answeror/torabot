from . import bp
from ..celery import sync_all as task_sync_all


@bp.route('/sync')
def sync():
    task_sync_all.delay()
    return 'done'
