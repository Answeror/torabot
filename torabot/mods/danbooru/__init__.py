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

    @staticmethod
    def tags(post):
        return post.tag_string

    @staticmethod
    def preview_url(post):
        if 'preview_file_url' not in post:
            return None
        return urljoin('http://danbooru.donmai.us/', post.preview_file_url)
