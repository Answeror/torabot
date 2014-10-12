import base64
from asyncio import coroutine
from ...celery import app as celery
from ..errors import LangError
from .base import Base


class Target(Base):

    unary = False

    @coroutine
    def __call__(self, **kargs):
        return (yield from _transform(**kargs))


@celery.async_task(name='xslt')
def _transform(**kargs):
    import lxml.etree as ET
    data, xslt, parser = _parse_args(kargs)
    html = ET.XML(data, parser)
    xslt = ET.XML(xslt)
    transform = ET.XSLT(xslt)
    feed = transform(html)
    s = ET.tostring(feed, pretty_print=True)
    return s.decode('utf-8') if s is not None else str(feed)


def _parse_args(kargs):
    import lxml.etree as ET
    parser_makers = {
        'xml': ET.XMLParser,
        'html': ET.HTMLParser,
    }
    xslt = kargs.get('xslt_encoded')
    if xslt is None:
        text = kargs.get('xslt')
        if text is not None:
            xslt = text.encode('utf-8')
    else:
        xslt = base64.b64decode(xslt)

    for name in parser_makers:
        data = kargs.get(name + '_encoded')
        if data is None:
            text = kargs.get(name)
            if text is not None:
                data = text.encode('utf-8')
        else:
            data = base64.b64decode(data)
        if data:
            return data, xslt, parser_makers[name]()

    raise LangError('unknown input type of xslt')
