from nose.tools import assert_equal
from .mixin import ModelMixin
from ..model import Session, Art, Change


class TestModel(ModelMixin):

    def setup(self):
        ModelMixin.setup(self)
        self.session = Session()

    def teardown(self):
        self.session.close()
        ModelMixin.teardown(self)

    def test_add_art(self):
        self.session.add(Art(
            title='foo',
            author='bar',
            company='foobar',
            toraid='123456789012',
            state=Art.RESERVE,
        ))
        self.session.commit()
        assert_equal(self.session.query(Art).count(), 1)

    def test_add_change(self):
        art = Art(
            title='foo',
            author='bar',
            company='foobar',
            toraid='123456789012',
            state=Art.RESERVE,
        )
        self.session.add(art)
        self.session.commit()
        self.session.add(Change(art=art, what=Change.NEW))
        self.session.commit()
        assert_equal(self.session.query(Change).count(), 1)
