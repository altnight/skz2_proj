from bpmappers.djangomodel import *
from bpmappers import RawField, Mapper, DelegateField, ListDelegateField
from skz2.models import Tweet, Lists

class TweetMapper(ModelMapper):
    class Meta:
        model = Tweet
        exclude = 'user', 'ctime', 'created_at'

class ListsMapper(ModelMapper):
    class Meta:
        model = Lists
        exclude = 'user', 'ctime', 'atime'

class RateLimit(object):
    def __init__(self, remaining, hourly_limit, reset_time):
        self.remaining = remaining
        self.hourly_limit = hourly_limit
        self.reset_time = reset_time

class RateLimitMapper(Mapper):
    remaining = RawField()
    hourly_limit = RawField()
    reset_time = RawField()
