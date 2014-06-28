import base64
from .base import Base


class Target(Base):

    def __call__(self, text):
        return base64.b64decode(text).decode(
            self.options.get('encoding', 'utf-8')
        )
