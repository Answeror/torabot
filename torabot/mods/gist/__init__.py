from ..base import Core
from ..mixins import (
    ScrapyMixin,
    NoChangeMixin,
    PostgreSQLBackend,
)


class Gist(
    ScrapyMixin,
    NoChangeMixin,
    PostgreSQLBackend,
    Core
):
    name = 'gist'
