import execjs
from .base import Base


class Target(Base):

    unary = False

    def __call__(self, code, args):
        node = execjs.get('Node')
        context = node.compile(code)
        return context.call(*args)
