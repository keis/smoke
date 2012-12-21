import unittest
import mock
from smoke import signal, Broker, Disconnect, StopPropagation


class Source(object):
    spam = signal()
    egg = signal(name='egg')


class Mixed(Source, Broker):
    pass


class TestMixed(unittest.TestCase):
    def setUp(self):
        self.listener = mock.Mock()
        self.mixed = Mixed()

    def test_subscribe_signal_publish_broker(self):
        sentinel = object()
        self.mixed.spam.subscribe(self.listener.spam_cb)
        self.mixed.publish(self.mixed.spam, s=sentinel)
        self.listener.spam_cb.assert_called_once_with(s=sentinel)

    def test_subscribe_broker_publish_signal(self):
        sentinel = object()
        self.mixed.subscribe(self.mixed.spam, self.listener.spam_cb)
        self.mixed.spam(s=sentinel)
        self.listener.spam_cb.assert_called_once_with(s=sentinel)

    def test_subscribe_by_name(self):
        sentinel = object()
        self.mixed.subscribe('egg', self.listener.egg_cb)
        self.mixed.egg(s=sentinel)
        self.listener.egg_cb.assert_called_once_with(s=sentinel)

    def test_publish_by_name(self):
        sentinel = object()
        self.mixed.egg.subscribe(self.listener.egg_cb)
        self.mixed.publish('egg', s=sentinel)
        self.listener.egg_cb.assert_called_once_with(s=sentinel)
