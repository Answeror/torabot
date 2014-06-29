import base64
from .base import Base


class Target(Base):

    def __call__(self, text, encoding='utf-8'):
        return base64.b64decode(text).decode(encoding)
