import json
import base64
import jsonpickle
from flask import current_app, abort, request
from logbook import Logger
from ...core.backends.redis import Redis
from ...core.make.task import Task
from ...core.mod import mod
from . import bp


log = Logger(__name__)


@bp.route('/gist/<id>', methods=['GET'])
def gist(id):
    log.debug('gist %s search start' % id)
    q = mod('gist').search(
        text=json.dumps(dict(method='id', id=id)),
        timeout=current_app.config['TORABOT_SPY_TIMEOUT'],
        sync_on_expire=True,
        backend=Redis()
    )
    log.debug('gist %s search done' % id)
    if not q:
        abort(503)

    files = q.result.files
    for f in files:
        if f['name'] == 'torabot.json':
            targets = jsonpickle.decode(
                base64.b64decode(f['content']).decode('utf-8')
            )['targets']
            break
    else:
        targets = None

    if not targets:
        abort(404)

    task = Task.from_string(jsonpickle.encode({
        'targets': targets,
        'files': files
    }), kargs={key: request.args[key] for key in request.args})
    return task()
