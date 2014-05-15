from ...ut.bunch import bunchr
from .query import get_query_text


class BooruMixin(object):

    def view(self, name):
        from .views import web, email
        return {
            'web': web.WebView(
                display_name=self.display_name,
                post_uri_template=self.post_uri_template,
                posts_url=self.posts_url,
                tags=self.tags,
                preview_url=self.preview_url,
            ),
            'email': email.EmailView(
                display_name=self.display_name,
                post_uri_template=self.post_uri_template,
                referer=self.referer,
                tags=self.tags,
                preview_url=self.preview_url,
            ),
        }[name]

    def changes(self, old, new):
        oldmap = {post.id: post for post in getattr(old, 'posts', [])}
        for post in new.posts:
            if post.id not in oldmap:
                yield bunchr(
                    kind='post.new',
                    post=post,
                    query_text=get_query_text(new.query)
                )

    def spy(self, query, timeout):
        from .query import regular
        result = super(BooruMixin, self).spy(regular(query), timeout)
        result.posts = [p for p in result.posts if self.preview_url(p)]
        return result
