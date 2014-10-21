from asyncio import get_event_loop
from .alask import Alask


class App(Alask):

    @property
    def loop(self):
        value = getattr(self, '_loop', None)
        if value is None:
            self._loop = value = get_event_loop()
        return value


__all__ = ['App']
