import requests
from ....ut.bunch import Bunch


class EmailView(object):

    def __init__(
        self,
        display_name,
        post_uri_template,
        referer,
        tags,
        preview_url,
    ):
        self.display_name = display_name
        self.post_uri_template = post_uri_template
        self.referer = referer
        self.tags = tags
        self.preview_url = preview_url

    def format_new_post_notice(self, notice):
        return '\n'.join([
            self.display_name,
            '---',
            'query: %(query)s',
            'uri: %s' % (self.post_uri_template.format(notice.change.post.id)),
            'tags: %(tags)s',
        ]) % dict(
            query=notice.change.query_text,
            tags=self.tags(notice.change.post),
        )

    def format_notice_body(self, notice):
        return {
            'post.new': self.format_new_post_notice,
        }[notice.change.kind](notice)

    def notice_attachments(self, notice):
        return {
            'post.new': self.new_post_notice_attachments,
        }[notice.change.kind](notice)

    def new_post_notice_attachments(self, notice):
        r = requests.get(
            self.preview_url(notice.change.post),
            headers=dict(referer=self.referer)
        )
        return [Bunch(
            name=self.tags(notice.change.post),
            mime=r.headers['content-type'],
            data=r.content,
        )]
