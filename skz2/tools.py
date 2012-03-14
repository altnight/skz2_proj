#-*- coding: utf-8 -*-
from skz2.models import User

from config import TwitterOAuth

import tweepy

CONSUMER_KEY = TwitterOAuth.consumer_key
CONSUMER_SECRET = TwitterOAuth.consumer_secret
CALLBACK_URL = TwitterOAuth.callback_url

def setOAauth(request):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(request.session.get('access_token_key'), request.session.get('access_token_secret'))
    return auth
