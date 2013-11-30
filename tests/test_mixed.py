import mock
from hamcrest import assert_that, equal_to
from smoke import signal, Broker, Disconnect, StopPropagation
from tests.matchers import called_once_with


class Source(object):
    spam = signal()
    egg = signal(name='egg')


class Mixed(Source, Broker):
    pass


class TestMixed(object):
    def setUp(self):
        self.listener = mock.Mock()
        self.mixed = Mixed()

    def test_subscribe_signal_publish_broker(self):
        sentinel = object()
        self.mixed.spam.subscribe(self.listener.spam_cb)
        self.mixed.publish(self.mixed.spam, s=sentinel)

        assert_that(self.listener.spam_cb, called_once_with(s=sentinel))

    def test_subscribe_broker_publish_signal(self):
        sentinel = object()
        self.mixed.subscribe(self.mixed.spam, self.listener.spam_cb)
        self.mixed.spam(s=sentinel)

        assert_that(self.listener.spam_cb, called_once_with(s=sentinel))

    def test_subscribe_broker_publish_signal_with_name(self):
        sentinel = object()
        self.mixed.subscribe(self.mixed.egg, self.listener.egg_cb)
        self.mixed.egg(s=sentinel)

        assert_that(self.listener.egg_cb, called_once_with(s=sentinel))

    def test_subscribe_by_name(self):
        sentinel = object()
        self.mixed.subscribe('egg', self.listener.egg_cb)
        self.mixed.egg(s=sentinel)

        assert_that(self.listener.egg_cb, called_once_with(s=sentinel))

    def test_publish_override(self):
        sentinel = object()
        self.mixed.publish = mock.Mock(wraps=self.mixed.publish)
        self.mixed.egg(s=sentinel)
        assert_that(self.mixed.publish, called_once_with(self.mixed.egg, s=sentinel))
