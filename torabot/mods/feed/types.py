from email.utils import formataddr
from datetime import datetime
import time
from ...ut.time import TIME_DISPLAY_FORMAT


class Wrap(object):

    def __init__(self, impl):
        self.impl = impl

    def __getattr__(self, name):
        return getattr(self.impl, name)

    def __contains__(self, value):
        return value in self.impl


class Feed(Wrap):

    @property
    def entries(self):
        return [Entry(e) for e in self.impl.entries]


class Change(Wrap):

    @property
    def data(self):
        return Feed(self.impl.data)

    @property
    def entry(self):
        return Entry(self.impl.entry)


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
        return self.best_content.type in ('text/html', 'application/xhtml+xml')

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

    def _make_best_content_text(self):
        return self._html2text(
            self.best_content.value,
            default=self.get('link', '')
        ) if self.is_html else self.best_content.value

    @property
    def best_content_text(self):
        name = '_best_content_text'
        value = getattr(self, name, None)
        if value is None:
            value = self._make_best_content_text()
            setattr(self, name, value)
        return value

    def _html2text(self, html, baseurl='', default=None):
        import html2text as _html2text
        import html.parser as _html_parser
        try:
            return _html2text.html2text(html=html, baseurl=baseurl)
        except _html_parser.HTMLParseError:
            if default is not None:
                return default
            raise

    @property
    def published_parsed(self):
        return time_to_datetime(self.impl.published_parsed)

    @property
    def published_parsed_display(self):
        return self.published_parsed.strftime(TIME_DISPLAY_FORMAT)

    @property
    def updated_parsed(self):
        return time_to_datetime(self.impl.updated_parsed)

    @property
    def updated_parsed_display(self):
        return self.updated_parsed.strftime(TIME_DISPLAY_FORMAT)


class Notice(Wrap):

    @property
    def change(self):
        return Change(self.impl.change)


class Query(Wrap):

    @property
    def result(self):
        return Result(self.impl.result)


class Result(Wrap):

    @property
    def data(self):
        return Feed(self.impl.data)


def time_to_datetime(t):
    return datetime.fromtimestamp(time.mktime(tuple(t)))
