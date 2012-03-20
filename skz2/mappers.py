from bpmappers.djangomodel import *
from skz2.models import Tweet

class TweetMapper(ModelMapper):
    class Meta:
        model = Tweet
        exclude = 'user', 'ctime', 'created_at'
