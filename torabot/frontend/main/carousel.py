import os
import tempfile
import subprocess as sp
from urllib.parse import urljoin
from logbook import Logger
from ...core.mod import mods


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


log = Logger(__name__)


def snapshots():
    for mod in mods():
        yield dict(
            src=mod.carousel,
            file=os.path.join('images', mod.name + '.jpg')
        )


def take(uri, path):
    log.info('take {} into {}', uri, path)
    temp = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    temp.close()
    try:
        sp.check_call([
            'phantomjs',
            os.path.join(CURRENT_PATH, 'snapshot.js'),
            uri,
            temp.name
        ])
        sp.check_call([
            'convert',
            temp.name,
            '-crop',
            '1280x+320+0',
            '-blur',
            '0x1',
            '-quality',
            '50',
            path
        ])
    finally:
        os.unlink(temp.name)


def make_uri(src):
    return urljoin('http://localhost', src)


def make_path(file):
    return os.path.join(CURRENT_PATH, 'static', file)


def take_all():
    from ... import make
    app = make()
    with app.test_request_context():
        for snapshot in snapshots():
            take(make_uri(snapshot['src']), make_path(snapshot['file']))


def main():
    take_all()


if __name__ == '__main__':
    main()
