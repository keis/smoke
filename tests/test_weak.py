import gc
from smoke import weak, Disconnect
from tests.matchers import assert_raises
from hamcrest import assert_that, equal_to, instance_of


class Dummy(object):
    value = None

    def spam(self):
        return self.value


def test_weak_forwards_call():
    d = Dummy()
    d.value = 'spam'
    w = weak(d.spam)
    r = w()
    assert_that(r, equal_to(d.value))


def test_weak_raises_disconnect():
    d = Dummy()
    w = weak(d.spam)
    del d
    gc.collect()

    with assert_raises(instance_of(Disconnect)):
        w()
