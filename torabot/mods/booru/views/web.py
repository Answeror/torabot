from flask import render_template
from ..query import parse as parse_query


class WebView(object):

    def __init__(
        self,
        display_name,
        post_uri_template,
        posts_url,
    ):
        self.display_name = display_name
        self.post_uri_template = post_uri_template

    def format_query_result(self, query):
        return {
            'posts_uri': self.format_posts_result,
            'query': self.format_posts_result,
        }[parse_query(query.text).method](query)

    def format_posts_result(self, query):
        return render_template(
            'booru/result/posts.html',
            query=query,
            post_uri_template=self.post_uri_template,
        )

    def format_new_post_notice(self, notice):
        return "<span class='label label-primary'>%(display_name)s</span>查询%(sep)s%(query)s%(sep)s更新了<a href='%(post_uri)s'>新作品</a>%(sep)s" % dict(
            query=notice.change.query_text,
            sep='<span class=w-d5em></span>',
            display_name=self.display_name,
            post_uri=self.post_uri_template.format(notice.change.post.id),
        )

    def format_notice_body(self, notice):
        return {
            'post.new': self.format_new_post_notice,
        }[notice.change.kind](notice)

    def format_help_page(self):
        return render_template('booru/help.html', posts_url=self.posts_url)
