from ..base import Core
from ..mixins import IdentityGuessNameMixin


class Gist(
    IdentityGuessNameMixin,
    Core
):
    name = 'gist'

    def changes(self, old, new):
        pass
