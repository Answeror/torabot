from flask import Blueprint
from ...ut.bunch import Bunch
from ..base import Mod
from ..mixins import ViewMixin, NoEmptyQueryMixin, KanjiMixin


name = 'pixiv'
bp = Blueprint(
    name,
    __name__,
    static_folder='static',
    template_folder='templates',
    static_url_path='/%s/static' % name
)


class Pixiv(ViewMixin, NoEmptyQueryMixin, KanjiMixin, Mod):

    name = 'pixiv'
    display_name = 'pixiv'
    has_advanced_search = True
    blueprint = bp

    def view(self, name):
        from .views import web, email
        return {
            'web': web,
            'email': email,
        }[name]

    def changes(self, old, new):
        oldmap = {art.uri: art for art in getattr(old, 'arts', [])}
        for art in new.arts:
            if art.uri not in oldmap:
                yield Bunch(kind='new', art=art)

    def spy(self, query, timeout):
        from .query import regular
        return super(Pixiv, self).spy(regular(query), timeout)
