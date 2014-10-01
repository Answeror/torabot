from .base import Base


class Target(Base):

    unary = False

    def __call__(self, *args):
        return args[-1]
