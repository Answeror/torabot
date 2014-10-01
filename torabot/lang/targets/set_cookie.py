import requests
import time
from http.cookies import SimpleCookie
from .base import Base
from .request import isuri
import requests.cookies


def morsel_to_cookie(morsel):
    """Convert a Morsel object into a Cookie containing the one k/v pair."""

    expires = None
    if morsel['max-age']:
        expires = time.time() + float(morsel['max-age'])
    elif morsel['expires']:
        time_template = '%a, %d-%b-%Y %H:%M:%S GMT'
        expires = time.mktime(
            time.strptime(morsel['expires'], time_template)) - time.timezone
    return requests.cookies.create_cookie(
        comment=morsel['comment'],
        comment_url=bool(morsel['comment']),
        discard=False,
        domain=morsel['domain'],
        expires=expires,
        name=morsel.key,
        path=morsel['path'],
        port=None,
        rest={'HttpOnly': morsel['httponly']},
        rfc2109=False,
        secure=bool(morsel['secure']),
        value=morsel.value,
        version=morsel['version'] or 0,
    )


requests.cookies.morsel_to_cookie = morsel_to_cookie


class Target(Base):

    unary = False

    def __call__(self, request, set_cookie):
        assert isinstance(set_cookie, str) or isinstance(set_cookie, list), str(set_cookie)
        if isuri(request):
            request = {'uri': request}
        jar = request.get('cookies', requests.cookies.RequestsCookieJar())
        headers = request.get('headers', {})
        cookie = headers.get('Cookie')
        if cookie:
            jar.update(SimpleCookie(cookie))
            del headers['Cookie']
        cookies = [set_cookie] if isinstance(set_cookie, str) else set_cookie
        for cookie in cookies:
            jar.update(SimpleCookie(cookie))
        request['cookies'] = jar
        return request
