from contextlib import contextmanager
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest import assert_that, instance_of


class RaisesContext(object):
    pass


@contextmanager
def assert_raises(matcher=None, message=''):
    # Short hand for instance_of matcher
    if isinstance(matcher, (type,)):
        matcher = instance_of(matcher)

    context = RaisesContext()
    try:
        yield context
    except Exception as e:
        context.exception = e

    assert_that(context.exception, matcher, message)


class called_with(BaseMatcher):
    def __init__(self, *args, **kwargs):
        self.args = (args, kwargs)

    def _matches(self, item):
        return item.call_args == self.args

    def describe_to(self, desc):
        args, kwargs = self.args
        desc.append_text('called with %r, %r' % (args, kwargs))


class called_once_with(called_with):
    def _matches(self, item):
        return item.call_count == 1 and called_with._matches(self, item)

    def describe_to(self, desc):
        args, kwargs = self.args
        desc.append_text('called once with %r, %r' % (args, kwargs))
