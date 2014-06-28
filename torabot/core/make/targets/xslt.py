import lxml.etree as ET
from .base import Base


PARSER_MAKERS = {
    'xml': ET.XMLParser,
    'html': ET.HTMLParser,
}


class Target(Base):

    def __call__(self, text, type):
        html = ET.XML(text.encode('utf-8'), PARSER_MAKERS[type]())
        xslt = ET.XML(self.read(self.options['xslt']))
        transform = ET.XSLT(xslt)
        feed = transform(html)
        return ET.tostring(feed, pretty_print=True).decode('utf-8')
