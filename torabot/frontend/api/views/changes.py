from flask import abort, request
from .. import bp
from ..ut import make


@bp.route('/source/<gist>', methods=['POST'])
def changes(gist):
    result = make(gist=gist, args=request.json)

    if isinstance(result, int):
        abort(result)

    return result, 200, {
        'content-type': 'application/json'
    }
