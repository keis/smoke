import mock
from hamcrest import assert_that, equal_to
from matchmock import called_once_with
from smoke import signal, publish, subscribe, Disconnect, StopPropagation


class Source(object):
    pass


def test_calls_subscribed():
    sentinel = object()
    source = Source()
    listener = mock.Mock()

    subscribe(source, 'spam', listener.spam_cb)
    publish(source, 'spam', s=sentinel)

    assert_that(listener.spam_cb, called_once_with(s=sentinel))


def test_free_signal():
    sentinel = object()
    source = Source()
    listener = mock.Mock()
    sig = signal('spam')

    subscribe(source, 'spam', listener.spam_cb)
    sig(source, s=sentinel)

    assert_that(listener.spam_cb, called_once_with(s=sentinel))
