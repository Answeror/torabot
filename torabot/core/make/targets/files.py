from .base import Base


class Target(Base):

    def __call__(self):
        return {
            'read': self.read,
            'read_text': self.read_text,
            'read_json': self.read_json,
        }
