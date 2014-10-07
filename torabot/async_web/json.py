import json


def jsonify(*args, **kargs):
    return (
        json.dumps(dict(*args, **kargs)),
        200,
        {'content-type': 'application/json; charset=utf-8'}
    )
