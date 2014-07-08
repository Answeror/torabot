import json
import base64
import jinja2
import jsonpickle
from nose.tools import assert_in
from flask import current_app, abort, request, jsonify
from logbook import Logger
from celery.exceptions import SoftTimeLimitExceeded
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
def source(id, format):
    args = {key: request.args[key] for key in request.args}
    log.info('source {} with args: {}', id, args)

    if format not in MIME:
        return jsonify({"message": "invalid format"}), 400

    q = mod('gist').search(
        text=json.dumps(dict(method='id', id=id)),
        timeout=current_app.config['TORABOT_SPY_TIMEOUT'],
        sync_on_expire=True,
        backend=Redis()
    )
    if not q:
        abort(502)

    files = q.result.files
    for f in files:
        if f['name'] == 'torabot.json':
            conf = jsonpickle.decode(jinja2.Template(
                base64.b64decode(f['content']).decode('utf-8')
            ).render(**args))
            break
    else:
        conf = None

    if not conf:
        abort(404)

    assert_in(format, MIME)
    try:
        return celery.make_source.apply_async(
            args=[files, conf],
            time_limit=current_app.config['TORABOT_MAKE_TIMEOUT'],
            soft_time_limit=current_app.config['TORABOT_MAKE_SOFT_TIMEOUT']
        ).get(), 200, {
            'content-type': MIME[format]
        }
    except SoftTimeLimitExceeded:
        log.warning('source soft timeout, {} with args: {}', id, args)
        abort(502)
