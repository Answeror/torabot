import json
import base64
import jinja2
import jsonpickle
from flask import current_app, abort, request
from logbook import Logger
from ...core.backends.redis import Redis
from ...core.make.targets import Target
from ...core.make.envs.dict import Env
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
            conf = jsonpickle.decode(jinja2.Template(
                base64.b64decode(f['content']).decode('utf-8')
            ).render(**{key: request.args[key] for key in request.args}))
            break
    else:
        conf = None

    if not conf:
        abort(404)

    return Target.run(Env(files), conf)
