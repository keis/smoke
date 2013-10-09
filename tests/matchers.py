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

    def describe_call(self, call, desc):
        args, kwargs = call
        desc.append_value(args)
        desc.append_text(', ')
        desc.append_value(kwargs)

    def describe_mismatch(self, item, mismatch_description):
        mismatch_description.append_text('was called with ')
        self.describe_call(item.call_args, mismatch_description)

    def describe_to(self, desc):
        desc.append_text('mock called with ')
        self.describe_call(self.args, desc)


class called_once_with(called_with):
    def _matches(self, item):
        return item.call_count == 1 and called_with._matches(self, item)

    def describe_mismatch(self, item, mismatch_description):
        if item.call_count != 1:
            mismatch_description.append_text(
                'was called %s times' % item.call_count)
        else:
            called_with.describe_mismatch(self, item, mismatch_description)

    def describe_to(self, desc):
        desc.append_text('mock called once with ')
        self.describe_call(self.args, desc)
