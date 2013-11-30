from smoke import signal, boundsignal
import mock
from hamcrest import assert_that, instance_of, equal_to, is_not, has_property
from tests.matchers import called_once_with, assert_raises


class Source(object):
    pass


def test_define_parameterised():
    change = signal('change', 'attribute')

    assert_that(change, instance_of(signal))


def test_define_parameterisation():
    change = signal('change', 'attribute')
    p = change('name')
    q = change('name')

    assert_that(p, instance_of(signal))
    assert_that(p, equal_to(q))

    assert_that(hash(p), equal_to(hash(q)))


def test_empty_parameters_compare_equal_to_parent():
    change = signal('change', 'attribute')
    p = change()

    assert_that(p, equal_to(change))


def test_different_parameterisations_compare_unequal():
    change = signal('change', 'attribute')
    p = change('name')
    q = change('age')

    assert_that(p, is_not(equal_to(q)))


def test_lookup():
    change = signal('change', 'attribute')
    d = {}
    sentinel = object()

    d[change('name')] = sentinel
    assert_that(d[change('name')], equal_to(sentinel))


def test_lookup_bound():
    class Foo(object):
        change = signal('change', 'attribute')
    f = Foo()

    d = {}
    sentinel = object()

    d[f.change('name')] = sentinel
    assert_that(d[f.change('name')], equal_to(sentinel))


def test_define_parameterisation_from_bound():
    class Foo(object):
        change = signal('change', 'attribute')
        cname = change('name')

    f = Foo()

    p = f.change('name')
    q = f.change('age')

    assert_that(p, instance_of(boundsignal))
    assert_that(p, is_not(equal_to(q)))
    assert_that(p, equal_to(f.cname))
