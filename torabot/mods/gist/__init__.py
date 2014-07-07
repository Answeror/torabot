from ..base import Core
from ..mixins import (
    ScrapyMixin,
    NoChangeMixin,
)


class Gist(
    ScrapyMixin,
    NoChangeMixin,
    Core
):
    name = 'gist'

    def regular(self, query_text):
        return self.name, query_text
