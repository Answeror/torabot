from .base import Base


class Target(Base):

    def __call__(self, name):
        none = object()
        value = self.env.result.get(name, none)
        if value is none:
            raise Exception('result of %s haven\'t been computed' % name)
        return value
