import json
import base64
from flask import request, abort
from logbook import Logger
from ...core.backends.redis import Redis
from ...core.mod import mod
from . import bp


log = Logger(__name__)


def _thumbnail_proxy(uri, referer):
    return mod('onereq').search(
        json.dumps({
            'uri': uri,
            'headers': {
                'referer': referer
            }
        }),
        timeout=10,
        sync_on_expire=False,
        backend=Redis()
    )


@bp.route('/thumb', methods=['GET'])
def thumbnail_proxy():
    log.debug(
        'thumbnail (uri, referer): ({}, {})',
        request.args['uri'],
        request.args['referer']
    )
    q = _thumbnail_proxy(request.args['uri'], request.args['referer'])
    if not q:
        abort(404)
    r = q.result
    return base64.b64decode(r.body), 200, {
        key: r.headers[key] for key in [
            'Content-Length',
            'Content-Type',
            'Date',
            'Expires',
            'Last-Modified',
        ] if key in r.headers
    }
