import unittest
import mock
from sig import Broker, Disconnect, StopPropagation


class TestBroker(unittest.TestCase):
    def setUp(self):
        self.listener = mock.Mock()
        self.broker = Broker()

    def test_calls_subscribed(self):
        event = 'test'
        sentinel = object()
        self.broker.subscribe(event, self.listener.test_cb)
        self.broker.publish(event, s=sentinel)
        self.listener.test_cb.assert_called_once_with(s=sentinel)

    def test_disconnect(self):
        event = 'test'
        self.broker.subscribe(event, self.listener.test_cb)
        self.broker.subscribe(event, self.listener.test2_cb)
        self.broker.publish(event)

        self.broker.disconnect(event, self.listener.test_cb)
        self.broker.publish(event)
        
        self.assertEqual(1, self.listener.test_cb.call_count)
        self.assertEqual(2, self.listener.test2_cb.call_count)

    def test_disconnect_exc(self):
        event = 'test'
        self.listener.spam_cb = mock.Mock(side_effect=Disconnect)
        self.broker.subscribe(event, self.listener.spam_cb)
        self.broker.subscribe(event, self.listener.spam_cb2)
        self.broker.publish(event)
        self.broker.publish(event)
        self.assertEqual(1, self.listener.spam_cb.call_count)
        self.assertEqual(2, self.listener.spam_cb2.call_count)

    def test_stop_exc(self):
        event = 'test'
        self.listener.spam_cb = mock.Mock(side_effect=StopPropagation)
        self.broker.subscribe(event, self.listener.spam_cb)
        self.broker.subscribe(event, self.listener.spam_cb2)
        self.broker.publish(event)
        self.assertEqual(1, self.listener.spam_cb.call_count)
        self.assertEqual(0, self.listener.spam_cb2.call_count)


