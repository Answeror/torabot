from .base import Base


class Target(Base):

    unary = False

    def __call__(self, cont, key, *args):
        for k in [key] + list(args):
            if k not in cont:
                raise Exception('{} not in {}'.format(k, cont))
            cont = cont[k]
        return cont
