import mock
from hamcrest import assert_that, equal_to
from matchmock import called_once_with
from smoke import Broker, Disconnect, StopPropagation


class TestBroker(object):
    def setUp(self):
        self.listener = mock.Mock()
        self.broker = Broker()

    def test_calls_subscribed(self):
        event = 'test'
        sentinel = object()
        self.broker.subscribe(event, self.listener.test_cb)
        self.broker.publish(event, s=sentinel)

        assert_that(self.listener.test_cb, called_once_with(s=sentinel))

    def test_disconnect(self):
        event = 'test'
        self.broker.subscribe(event, self.listener.test_cb)
        self.broker.subscribe(event, self.listener.test2_cb)
        self.broker.publish(event)

        self.broker.disconnect(event, self.listener.test_cb)
        self.broker.publish(event)

        assert_that(self.listener.test_cb.call_count, equal_to(1))
        assert_that(self.listener.test2_cb.call_count, equal_to(2))

    def test_disconnect_exc(self):
        event = 'test'
        self.listener.spam_cb = mock.Mock(side_effect=Disconnect)

        self.broker.subscribe(event, self.listener.spam_cb)
        self.broker.subscribe(event, self.listener.spam_cb2)
        self.broker.publish(event)
        self.broker.publish(event)

        assert_that(self.listener.spam_cb.call_count, equal_to(1))
        assert_that(self.listener.spam_cb2.call_count, equal_to(2))

    def test_stop_exc(self):
        event = 'test'
        self.listener.spam_cb = mock.Mock(side_effect=StopPropagation)
        self.broker.subscribe(event, self.listener.spam_cb)
        self.broker.subscribe(event, self.listener.spam_cb2)
        self.broker.publish(event)

        assert_that(self.listener.spam_cb.call_count, equal_to(1))
        assert_that(self.listener.spam_cb2.call_count, equal_to(0))

