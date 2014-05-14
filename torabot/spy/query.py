import json
from hashlib import md5


def hash(query):
    return md5(order(query).encode('utf-8')).hexdigest()


def order(query):
    if not isinstance(query, dict):
        try:
            d = json.loads(query)
            if not isinstance(d, dict):
                raise Exception('not standard')
            query = d
        except:
            return query
    assert isinstance(query, dict)
    return json.dumps(query, sort_keys=True)
