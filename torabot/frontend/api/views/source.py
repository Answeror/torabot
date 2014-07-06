import json
import base64
import jinja2
import jsonpickle
from nose.tools import assert_in
from flask import current_app, abort, request, jsonify
from logbook import Logger
from ....core.backends.redis import Redis
from ....core.mod import mod
from .... import celery
from .. import bp


log = Logger(__name__)


MIME = {
    'txt': 'text/plain',
    'json': 'application/json',
    'xml': 'text/xml',
    'atom': 'application/atom+xml',
    'rss': 'application/rss+xml',
    'html': 'text/html',
}


@bp.route('/source/<id>', methods=['GET'], defaults={'format': 'txt'})
@bp.route('/source/<id>.<format>', methods=['GET'])
def gist(id, format):
    log.debug('gist %s search start' % id)

    if format not in MIME:
        return jsonify({"message": "invalid format"}), 400

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

    assert_in(format, MIME)
    return celery.make_source.apply_async(
        args=[files, conf],
        time_limit=30,
        soft_time_limit=25
    ).get(), 200, {
        'content-type': MIME[format]
    }
