from urllib.parse import urljoin
from ..base import Mod
from ..mixins import (
    ViewMixin,
    make_blueprint_mixin
)
from ..booru.mixins import BooruMixin


name = 'danbooru'


class Danbooru(
    ViewMixin,
    BooruMixin,
    make_blueprint_mixin(__name__),
    Mod
):
    name = name
    display_name = 'danbooru'
    has_advanced_search = False
    description = '海量二次元图站, 订阅链接或关键字, 第一时间收图.'
    normal_search_prompt = '订阅地址/tags'
    allow_empty_query = True
    posts_url = 'http://danbooru.donmai.us/posts'
    post_uri_template = 'http://danbooru.donmai.us/posts/{}'
    referer = 'http://danbooru.donmai.us/'
    frontend_need_init = True

    @staticmethod
    def tags(post):
        return post.tag_string

    @staticmethod
    def preview_url(post):
        if 'preview_file_url' not in post:
            return None
        return urljoin('http://danbooru.donmai.us/', post.preview_file_url)

    def get(self, arg):
        if not isinstance(arg, dict):
            raise Exception('unknown arg type: {}'.format(type(arg)))
        return {
            'completion': self.get_completion
        }[arg['type']](arg)

    def get_completion(self, arg):
        import json
        from ...core.connection import autoccontext
        from ...core.local import get_current_conf
        from ...core.query import query
        with autoccontext(commit=True) as conn:
            q = query(
                conn=conn,
                kind=name,
                text=json.dumps(dict(method='tags', query=arg['query'])),
                timeout=get_current_conf()['TORABOT_SPY_TIMEOUT'],
            )
        return q.result.content

    @property
    def frontend_options(self):
        from flask import url_for
        return {
            'call_url': url_for("main.call", kind=name)
        }

    def spy(self, query, timeout):
        from ..booru.query import parse, regular
        if parse(query).method == 'tags':
            spy = super(BooruMixin, self).spy
        else:
            spy = super(Danbooru, self).spy
        return spy(regular(query), timeout)

    def changes(self, old, new):
        if new.query.method == 'tags':
            return
        yield from super(Danbooru, self).changes(old, new)
