from flask import request, abort
import requests
from logbook import Logger
from . import bp


log = Logger(__name__)


@bp.route('/thumbnail-proxy', methods=['GET'])
def thumbnail_proxy():
    log.info('uri: {}', request.args['uri'])
    log.info('referer: {}', request.args['referer'])
    r = requests.get(
        request.args['uri'],
        headers={
            'referer': request.args['referer']
        }
    )
    if not r.ok:
        abort(404)
    return r.content, 200, {
        key: r.headers[key] for key in [
            'content-length',
            'content-type',
            'date',
            'expires',
            'last-modified',
        ]
    }
