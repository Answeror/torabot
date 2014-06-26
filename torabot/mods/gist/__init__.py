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
