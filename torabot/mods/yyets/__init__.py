from ...ut.bunch import bunchr
from ..base import Mod
from ..mixins import (
    ViewMixin,
    NoEmptyQueryMixin,
    make_blueprint_mixin,
    IdentityGuessNameMixin,
    make_field_guess_name_mixin
)
from logbook import Logger


name = 'yyets'
log = Logger(__name__)


class Yyets(
    ViewMixin,
    NoEmptyQueryMixin,
    make_blueprint_mixin(__name__),
    make_field_guess_name_mixin('uri'),
    IdentityGuessNameMixin,
    Mod
):
    name = name
    display_name = '人人影视'
    has_advanced_search = False
    description = '电影/电视剧订阅(来自人人影视)'
    normal_search_prompt = '订阅地址'

    @property
    def carousel(self):
        from flask import url_for
        return url_for("main.example_search", kind=name, q="http://www.yyets.com/rss/feed/?area=%E7%BE%8E%E5%9B%BD")

    def view(self, name):
        from .views import web, email
        return {
            'web': web,
            'email': email
        }[name]

    def changes(self, old, new):
        oldmap = {art.guid: art for art in getattr(old, 'arts', [])}
        for art in new.arts:
            try:
                if art.guid not in oldmap:
                    yield bunchr(kind='rss.new', art=art)
            except:
                log.info(str(art))
                raise

    def spy(self, query, timeout):
        from .query import parse, regular
        query = parse(query)
        return super(Yyets, self).spy(regular(query), timeout)
