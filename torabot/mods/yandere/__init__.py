from ..base import Mod
from ..mixins import (
    ViewMixin,
    make_blueprint_mixin
)
from ..booru.mixins import BooruMixin


name = 'yandere'


class Yandere(
    ViewMixin,
    BooruMixin,
    make_blueprint_mixin(__name__),
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

    @staticmethod
    def tags(post):
        return post.tags

    @staticmethod
    def preview_url(post):
        return post.preview_url
