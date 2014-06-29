from .base import Base


class Target(Base):

    def __call__(self, *args):
        return args[-1]
