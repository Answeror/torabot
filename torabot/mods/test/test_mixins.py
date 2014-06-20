from nose.tools import assert_equal
from ...ut.bunch import Bunch
from ..base import Mod as Base
from ..mixins import IdentityGuessNameMixin, make_field_guess_name_mixin


def check_field_guess_name_mixin(query, desire):
    class Mod(make_field_guess_name_mixin('uri', 'query'), IdentityGuessNameMixin):
        pass
    mod = Mod()
    assert_equal(mod.guess_name(query), desire)


def test_field_guess_name_mixin():
    for query, desire in [
        (Bunch(text='foo'), 'foo'),
        (Bunch(text='{"method": "user_uri", "uri": "foo"}'), "foo"),
        (Bunch(text='{"method": "query", "query": "bar"}'), "bar"),
    ]:
        yield check_field_guess_name_mixin, query, desire


def test_identity_guess_name_mixin():
    class Mod(IdentityGuessNameMixin):
        pass
    mod = Mod()
    assert_equal(mod.guess_name(Bunch(text='foo')), 'foo')
