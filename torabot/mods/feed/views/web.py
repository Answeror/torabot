from flask import render_template
from email.utils import formataddr
from ....ut.bunch import bunchr
from ..query import parse as parse_query


class Wrap(object):

    def __init__(self, impl):
        self.impl = impl

    def __getattr__(self, name):
        return getattr(self.impl, name)


class Feed(Wrap):

    @property
    def entries(self):
        return [Entry(e) for e in self.impl.entries]


class Entry(Wrap):

    @property
    def formatted_author(self):
        if 'author' not in self:
            return ''
        name = self.author
        email = self.get('author_detail', {}).get('email', '')
        return formataddr((name, email)) if email else name

    @property
    def author_link(self):
        detail = self.get('author_detail', {})
        return 'mailto:' + detail.email if 'email' in detail else detail.get('href', '#')

    @property
    def link(self):
        return self.impl.get('link', '#')

    @property
    def title(self):
        return self.impl.title if self.impl.title.strip() else self.link

    @property
    def best_content_empty(self):
        return not self.best_content.value.strip()

    @property
    def is_html(self):
        if self.best_content.type not in ('text/html', 'application/xhtml+xml'):
            return False
        s = self.best_content.value.strip()
        return s and (s[0], s[-1]) == ('<', '>')

    def _make_best_content(self):
        """Select the best content from an entry.

        Returns a feedparser content dict.

        How this works:
         * We have a bunch of potential contents.
         * We go thru looking for our first choice.
           (HTML or text, depending on self.html_mail)
         * If that doesn't work, we go thru looking for our second choice.
         * If that still doesn't work, we just take the first one.

        Possible future improvement:
         * Instead of just taking the first one
           pick the one in the "best" language.
         * HACK: hardcoded .html_mail, should take a tuple of media types

        https://github.com/wking/rss2email/blob/master/rss2email/feed.py
        """
        contents = list(self.impl.get('content', []))
        if self.impl.get('summary_detail', None):
            contents.append(self.impl.summary_detail)
        for content_type in ['text/html', 'text/plain']:
            for content in contents:
                if content['type'] == content_type:
                    return content
        if contents:
            return contents[0]
        return {'type': 'text/plain', 'value': ''}

    @property
    def best_content(self):
        name = '_best_content'
        value = getattr(self, name, None)
        if value is None:
            value = self._make_best_content()
            setattr(self, name, value)
        return value

    def __contains__(self, value):
        return value in self.impl


def format_query_result(query):
    return {
        'uri': format_uri_result,
    }[parse_query(query.text).method](query)


def format_uri_result(query):
    query = bunchr(**query)
    query.result.data = Feed(query.result.data)
    return render_template('feed/result/uri.html', query=query)


def format_notice_body(notice):
    return {
        'uri.new': format_uri_notice
    }[notice.change.kind](notice)


def format_uri_notice(notice):
    return render_template('feed/notice/uri.html', notice=notice)


def format_help_page():
    return render_template('feed/help.html')
