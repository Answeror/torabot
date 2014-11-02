import base64
from ..celery import celery


@celery.async_task(name='xslt')
def xslt(**kargs):
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

    raise RuntimeError('unknown input type of xslt')


@celery.async_task(name='parse_html')
def parse_html(data, done):
    import lxml.etree as ET
    return done(ET.XML(data, ET.HTMLParser()))
