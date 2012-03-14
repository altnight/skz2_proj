#-*- coding: utf-8 -*-
from skz2.models import User

from config import TwitterOAuth

import tweepy

CONSUMER_KEY = TwitterOAuth.consumer_key
CONSUMER_SECRET = TwitterOAuth.consumer_secret
#CALLBACK_URL = TwitterOAuth.callback_url

def setOAuth(request):
    user = User.objects.get(name=request.session.get('session_user'))
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(user.access_token, user.access_token_secret)
    return auth
