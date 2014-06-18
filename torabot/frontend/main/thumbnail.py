from flask import request, abort
import requests
from logbook import Logger
from . import bp
from ...cache import cache


log = Logger(__name__)


@cache.memoize(timeout=600)
def _thumbnail_proxy(uri, referer):
    return requests.get(
        uri,
        headers={
            'referer': referer
        }
    )


@bp.route('/thumbnail-proxy', methods=['GET'])
def thumbnail_proxy():
    log.info('uri: {}', request.args['uri'])
    log.info('referer: {}', request.args['referer'])
    r = _thumbnail_proxy(request.args['uri'], request.args['referer'])
    if not r.ok:
        cache.delete_memoized(
            '_thumbnail_proxy',
            request.args['uri'],
            request.args['referer']
        )
        abort(404)
    return r.content, 200, {
        key: r.headers[key] for key in [
            'content-length',
            'content-type',
            'date',
            'expires',
            'last-modified',
        ] if key in r.headers
    }
