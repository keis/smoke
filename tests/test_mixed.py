import pytest
import mock
from hamcrest import assert_that
from matchmock import called_once_with
from smoke import signal, Broker


class Source(object):
    spam = signal()
    egg = signal(name='egg')


class Mixed(Source, Broker):
    pass


@pytest.fixture
def listener():
    return mock.Mock()


@pytest.fixture
def mixed():
    return Mixed()


def test_subscribe_signal_publish_broker(mixed, listener):
    sentinel = object()
    mixed.spam.subscribe(listener.spam_cb)
    mixed.publish(mixed.spam, s=sentinel)

    assert_that(listener.spam_cb, called_once_with(s=sentinel))


def test_subscribe_broker_publish_signal(mixed, listener):
    sentinel = object()
    mixed.subscribe(mixed.spam, listener.spam_cb)
    mixed.spam(s=sentinel)

    assert_that(listener.spam_cb, called_once_with(s=sentinel))


def test_subscribe_broker_publish_signal_with_name(mixed, listener):
    sentinel = object()
    mixed.subscribe(mixed.egg, listener.egg_cb)
    mixed.egg(s=sentinel)

    assert_that(listener.egg_cb, called_once_with(s=sentinel))


@pytest.mark.skip(reason="Not supported, for now")
def test_subscribe_signal_publish_boundsignal(mixed, listener):
    # Supporting this in a general way might be a bit to intrusive as
    # boundmethod and function and other things implementing the descriptor
    # protocol would be consider equal as well.

    sentinel = object()
    mixed.subscribe(Mixed.spam, listener.spam_cb)
    mixed.publish(mixed.spam, s=sentinel)

    assert_that(listener.spam_cb, called_once_with(s=sentinel))


def test_subscribe_by_name(mixed, listener):
    sentinel = object()
    mixed.subscribe('egg', listener.egg_cb)
    mixed.egg(s=sentinel)

    assert_that(listener.egg_cb, called_once_with(s=sentinel))


def test_publish_override(mixed, listener):
    sentinel = object()
    mixed.publish = mock.Mock(wraps=mixed.publish)
    mixed.egg(s=sentinel)
    assert_that(mixed.publish, called_once_with(mixed.egg, s=sentinel))
