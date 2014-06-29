import lxml.etree as ET
from .base import Base


PARSER_MAKERS = {
    'xml': ET.XMLParser,
    'html': ET.HTMLParser,
}


def get_text_and_parser(kargs):
    for name in PARSER_MAKERS:
        text = kargs.get(name)
        if text:
            return text, PARSER_MAKERS[name]()
    raise Exception('unknown input type of xslt')


class Target(Base):

    @Base.preprocessed
    def __call__(self, xslt, **kargs):
        text, parser = get_text_and_parser(kargs)
        html = ET.XML(text.encode('utf-8'), parser)
        xslt = ET.XML(xslt.encode('utf-8'))
        transform = ET.XSLT(xslt)
        feed = transform(html)
        return ET.tostring(feed, pretty_print=True).decode('utf-8')
