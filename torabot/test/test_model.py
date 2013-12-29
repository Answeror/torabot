from .g import g
from .mixin import ModelMixin
from ..model import Session, Art, Change
from .. import state
from .. import what
from nose.tools import assert_equal


class TestModel(ModelMixin):

    def test_add_art(self):
        s = Session()
        s.add(Art(
            title='foo',
            author='bar',
            comp='foobar',
            toraid='123456789012',
            state=state.RESERVE,
        ))
        s.commit()
        assert_equal(s.query(Art).count(), 1)

    def test_add_change(self):
        s = Session()
        art = Art(
            title='foo',
            author='bar',
            comp='foobar',
            toraid='123456789012',
            state=state.RESERVE,
        )
        s.add(art)
        s.commit()
        s.add(Change(art=art, what=what.NEW))
        s.commit()
        assert_equal(s.query(Change).count(), 1)
