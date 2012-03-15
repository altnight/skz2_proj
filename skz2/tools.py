#-*- coding: utf-8 -*-
from skz2.models import User
from config import TwitterOAuth

import tweepy

import re

CONSUMER_KEY = TwitterOAuth.consumer_key
CONSUMER_SECRET = TwitterOAuth.consumer_secret
#CALLBACK_URL = TwitterOAuth.callback_url

def setOAuth(request):
    """OAuthの設定の汎用化"""
    user = User.objects.get(name=request.session.get('session_user'))
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(user.access_token, user.access_token_secret)
    return auth

def expandURL(tweet):
    """t.coの展開"""
    text = tweet.text
    for url in tweet.entities['urls']:
        if url is None:
            continue
        else:
            for i in tweet.entities['urls']:
                if re.search(i['url'], text):
                    text = re.sub(i['url'], i['expanded_url'], text)
    return text
