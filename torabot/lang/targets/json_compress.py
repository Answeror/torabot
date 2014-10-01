import json
from .base import Base


class Target(Base):

    unary = True

    def __call__(self, text):
        return json.dumps(json.loads(text))
