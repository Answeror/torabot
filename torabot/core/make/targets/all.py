from .base import Base


class Target(Base):

    unary = True

    def __call__(self, *args):
        return args[-1]
