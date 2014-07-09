from logbook import Logger
from flask import current_app, abort, request, jsonify
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


@bp.route('/source/<gist>', methods=['GET'], defaults={'format': 'txt'})
@bp.route('/source/<gist>.<format>', methods=['GET'])
def source(gist, format):
    if format not in MIME:
        return jsonify({"message": "invalid format"}), 400

    args = {key: request.args[key] for key in request.args}
    log.info('source {} with {}', gist, args)

    result = celery.make_source.apply_async(
        kwargs=dict(gist=gist, args=args),
        expires=current_app.config['TORABOT_MAKE_SOFT_TIMEOUT'],
        time_limit=current_app.config['TORABOT_MAKE_TIMEOUT'],
        soft_time_limit=current_app.config['TORABOT_MAKE_SOFT_TIMEOUT']
    ).get(interval=0.1)

    if isinstance(result, int):
        abort(result)

    return result, 200, {
        'content-type': MIME[format]
    }
