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
