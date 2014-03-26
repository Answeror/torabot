import os
from ...ut.bunch import Bunch
from ..base import Mod
from ..mixins import ViewMixin, NoEmptyQueryMixin, KanjiMixin
from .views import web, email


ROOT = os.path.abspath(os.path.dirname(__file__))


class Pixiv(ViewMixin, NoEmptyQueryMixin, KanjiMixin, Mod):

    name = 'pixiv'
    display_name = 'pixiv'
    has_advanced_search = True
    template_folder = os.path.join(ROOT, 'views', 'templates')

    def view(self, name):
        return {
            'web': web,
            'email': email,
        }[name]

    def changes(self, old, new):
        oldmap = {art.uri: art for art in getattr(old, 'arts', [])}
        for art in new.arts:
            if art.uri not in oldmap:
                yield Bunch(kind='new', art=art)
