from .base import Base


class Target(Base):

    unary = True

    def __call__(self, conf):
        return Target.run(self.env, conf)
