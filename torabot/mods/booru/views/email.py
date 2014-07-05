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
        r = download(
            self.preview_url(notice.change.post),
            self.referer
        )
        import base64
        return [Bunch(
            name=self.tags(notice.change.post),
            mime=stringify(r.headers['Content-Type']),
            data=base64.b64decode(r.body),
        )]


def stringify(s):
    if isinstance(s, str):
        return s
    if isinstance(s, list):
        return s[0]
    raise Exception('cannot stringify {}'.format(s))


def download(uri, referer):
    import json
    from ....core.mod import mod
    from ....core.backends.redis import Redis
    q = mod('onereq').search(
        json.dumps({
            'uri': uri,
            'headers': {
                'referer': referer
            }
        }),
        timeout=30,
        sync_on_expire=False,
        backend=Redis()
    )
    if not q:
        raise Exception('download %s failed' % uri)
    return q.result
