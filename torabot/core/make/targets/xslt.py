import base64
import lxml.etree as ET
from .base import Base


PARSER_MAKERS = {
    'xml': ET.XMLParser,
    'html': ET.HTMLParser,
}


def parse_args(kargs):
    xslt = kargs.get('xslt_encoded')
    if xslt is None:
        text = kargs.get('xslt')
        if text is not None:
            xslt = text.encode('utf-8')
    else:
        xslt = base64.b64decode(xslt)

    for name in PARSER_MAKERS:
        data = kargs.get(name + '_encoded')
        if data is None:
            text = kargs.get(name)
            if text is not None:
                data = text.encode('utf-8')
        else:
            data = base64.b64decode(data)
        if data:
            return data, xslt, PARSER_MAKERS[name]()

    raise Exception('unknown input type of xslt')


class Target(Base):

    unary = False

    def __call__(self, **kargs):
        data, xslt, parser = parse_args(kargs)
        html = ET.XML(data, parser)
        xslt = ET.XML(xslt)
        transform = ET.XSLT(xslt)
        feed = transform(html)
        s = ET.tostring(feed, pretty_print=True)
        return s.decode('utf-8') if s is not None else str(feed)
