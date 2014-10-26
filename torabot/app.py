from asyncio import get_event_loop
from .alask import Alask


class App(Alask):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.parts = {}

        if not self.config.get('SECRET_KEY'):
            self.config['SECRET_KEY'] = 'test'

    @property
    def loop(self):
        value = getattr(self, '_loop', None)
        if value is None:
            self._loop = value = get_event_loop()
        return value


__all__ = ['App']
