from .base import Base


class Target(Base):

    def __call__(self, ping):
        return ping
