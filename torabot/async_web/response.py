import aiohttp
from aiohttp.protocol import EOF_MARKER, EOL_MARKER


class Response(aiohttp.Response):

    # Auto-send headers on write() calls
    _send_headers = True

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._length = 0
        self._request = request
        self.finished = False

    def set_status(self, status):
        self.status_line = Response(None, status).status_line
        self.status = status

    def write(self, chunk, close=False, unchunked=False):
        if isinstance(chunk, str):
            chunk = chunk.encode()

        if unchunked:
            self.add_header('CONTENT-LENGTH', str(len(chunk)))
            close = True

        super().write(chunk)

        if chunk not in [EOL_MARKER, EOF_MARKER]:
            self._length += len(chunk)

        if chunk is EOF_MARKER:
            close = False

        if close:
            self.write_eof()

    def redirect(self, location, status=302):
        self.set_status(status)
        self.add_header('Location', location)

    def write_eof(self):
        self.finished = True
        return super().write_eof()


__all__ = ['Response']
