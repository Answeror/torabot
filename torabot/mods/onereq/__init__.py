from ..base import Core
from ..mixins import (
    ScrapyMixin,
    NoChangeMixin,
    PostgreSQLBackend,
)
from .query import parse, regular


class Onereq(
    ScrapyMixin,
    NoChangeMixin,
    PostgreSQLBackend,
    Core
):
    name = 'onereq'

    def spy(self, query, timeout, options={}):
        return super(Onereq, self).spy(regular(query), timeout, options)['data']

    def sync_on_expire(self, query):
        return parse(query).get('options', {}).get('sync_on_expire', True)
