from ..base import Mod
from ..mixins import (
    ViewMixin,
    make_blueprint_mixin,
    IdentityGuessNameMixin,
    make_field_guess_name_mixin
)
from ..booru.mixins import BooruMixin


name = 'yandere'


class Yandere(
    ViewMixin,
    BooruMixin,
    make_blueprint_mixin(__name__),
    make_field_guess_name_mixin('uri', 'query'),
    IdentityGuessNameMixin,
    Mod
):
    name = name
    display_name = 'yande.re'
    has_advanced_search = False
    description = '二次元高清图站, 订阅链接或关键字, 第一时间收图.'
    normal_search_prompt = '订阅地址/tags'
    allow_empty_query = True
    posts_url = 'https://yande.re/post'
    post_uri_template = 'https://yande.re/post/show/{}'
    referer = 'https://yande.re/'
    frontend_need_init = True

    @property
    def carousel(self):
        from flask import url_for
        return url_for("main.example_search", kind=name, q="https://yande.re/post?tags=rating%3As")

    @staticmethod
    def tags(post):
        return post.tags

    @staticmethod
    def preview_url(post):
        return post.preview_url

    @property
    def frontend_options(self):
        from flask import url_for
        from ...core.local import get_current_conf
        return {
            'completion_options_uri': url_for("main.completion_options", kind=name),
            'completion_cache_timeout': get_current_conf()['TORABOT_MOD_YANDERE_COMPLETION_CACHE_TIMEOUT']
        }

    @property
    def completion_options(self):
        import json
        from ...core.backends.redis import Redis
        from ...core.local import get_current_conf
        from ..query import query
        q = query(
            kind=name,
            text=json.dumps(dict(method='tags')),
            timeout=get_current_conf()['TORABOT_SPY_TIMEOUT'],
            sync_on_expire=False,
            make_backend=lambda conn: Redis()
        )
        return q.content

    def spy(self, query, timeout):
        from ..booru.query import parse, regular
        if parse(query).method == 'tags':
            spy = super(BooruMixin, self).spy
        else:
            spy = super(Yandere, self).spy
        return spy(regular(query), timeout)

    def changes(self, old, new):
        if new.query.method == 'tags':
            return
        yield from super(Yandere, self).changes(old, new)

    def sync_on_expire(self, query):
        from ..booru.query import parse
        return parse(query.text).method != 'tags'
