from nose.tools import assert_equal
from .base import Base


class Target(Base):

    @Base.preprocessed
    def __call__(self, **kargs):
        values = list(kargs.values())
        assert_equal(len(values), 1)
        return values[0]
