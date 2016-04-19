import pytest
import mock
from hamcrest import assert_that, equal_to
from matchmock import called_once_with
from smoke import signal, Disconnect, StopPropagation


class Source(object):
    spam = signal()


@pytest.fixture
def listener():
    return mock.Mock()


@pytest.fixture
def source():
    return Source()


def test_calls_subscribed(source, listener):
    sentinel = object()

    source.spam.subscribe(listener.spam_cb)
    source.spam(s=sentinel)

    assert_that(listener.spam_cb, called_once_with(s=sentinel))


def test_disconnect(source, listener):
    source.spam.subscribe(listener.spam_cb)
    source.spam.subscribe(listener.spam2_cb)
    source.spam()

    source.spam.disconnect(listener.spam_cb)
    source.spam()

    assert_that(listener.spam_cb.call_count, equal_to(1))
    assert_that(listener.spam2_cb.call_count, equal_to(2))


def test_subscribe_on_bound(source, listener):
    bsignal = source.spam
    bsignal.subscribe(listener.spam_cb)
    source.spam()

    assert_that(listener.spam_cb, called_once_with())


def test_publish_on_bound(source, listener):
    source.spam.subscribe(listener.spam_cb)
    bsignal = source.spam
    bsignal()

    assert_that(listener.spam_cb, called_once_with())


def test_disconnect_on_bound(source, listener):
    bsignal = source.spam
    source.spam.subscribe(listener.spam_cb)
    source.spam.subscribe(listener.spam2_cb)
    source.spam()

    bsignal.disconnect(listener.spam_cb)
    source.spam()

    assert_that(listener.spam_cb.call_count, equal_to(1))
    assert_that(listener.spam2_cb.call_count, equal_to(2))


def test_subscribe_on_static(source, listener):
    Source.spam.subscribe(source, listener.spam_cb)
    source.spam()

    assert_that(listener.spam_cb, called_once_with())


def test_publish_on_static(source, listener):
    source.spam.subscribe(listener.spam_cb)
    Source.spam(source)
    listener.spam_cb.assert_called_once_with()


def test_disconnect_on_static(source, listener):
    source.spam.subscribe(listener.spam_cb)
    source.spam.subscribe(listener.spam2_cb)
    source.spam()

    Source.spam.disconnect(source, listener.spam_cb)
    source.spam()

    assert_that(listener.spam_cb.call_count, equal_to(1))
    assert_that(listener.spam2_cb.call_count, equal_to(2))


def test_disconnect_exc(source, listener):
    listener.spam_cb = mock.Mock(side_effect=Disconnect)
    source.spam.subscribe(listener.spam_cb)
    source.spam.subscribe(listener.spam_cb2)
    source.spam()
    source.spam()

    assert_that(listener.spam_cb.call_count, equal_to(1))
    assert_that(listener.spam_cb2.call_count, equal_to(2))


def test_stop_exc(source, listener):
    listener.spam_cb = mock.Mock(side_effect=StopPropagation)
    source.spam.subscribe(listener.spam_cb)
    source.spam.subscribe(listener.spam_cb2)
    source.spam()

    assert_that(listener.spam_cb.call_count, equal_to(1))
    assert_that(listener.spam_cb2.call_count, equal_to(0))
