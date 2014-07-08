from ..base import Core
from ..mixins import (
    ScrapyMixin,
    NoChangeMixin,
)
from .query import parse, regular


class Onereq(
    ScrapyMixin,
    NoChangeMixin,
    Core
):
    name = 'onereq'

    def spy(self, query, timeout, options={}):
        return super(Onereq, self).spy(regular(query), timeout, options)['data']

    def sync_on_expire(self, query):
        return parse(query).get('options', {}).get('sync_on_expire', True)

    def regular(self, query_text):
        from .query import regular
        return self.name, regular(query_text)

    @property
    def spy_slaves(self):
        return 1

    @property
    def spy_life(self):
        return 60 * 60
