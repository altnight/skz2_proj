#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
#from django.shortcuts import get_object_or_404

from skz2.models import User

import tweepy
from see import see

from config import TwitterOAuth
from skz2.tools import setOAauth
CONSUMER_KEY = TwitterOAuth.consumer_key
CONSUMER_SECRET = TwitterOAuth.consumer_secret
CALLBACK_URL = TwitterOAuth.callback_url

def index(request):
    if request.session.get('session_user'):
        return direct_to_template(request, "skz2.html",{})
    else:
        return direct_to_template(request, 'index.html',{})

def get_oauth(request):
    '''OAuthを取り付ける最初のステップ'''
    #CONSUMER_KEY,CONSUMER_SECRETを設定
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, CALLBACK_URL)
    try:
        auth_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print '401 Error! Failed to get request token.'
    request.session['request_token'] = (auth.request_token.key, auth.request_token.secret)
    return HttpResponseRedirect(auth_url)

def callback(request):
    ''' Callback '''
    #コールバックで戻ってくる
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    token = request.session.get('request_token')
    del request.session['request_token']
    auth.set_request_token(token[0], token[1])

    verifier = request.GET.get('oauth_verifier')
    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print 'Error! Failed to get access token.'

    request.session['access_token_key'] = auth.access_token.key
    request.session['access_token_secret'] = auth.access_token.secret

    if User.objects.filter(name=auth.get_username()):
        new_user = User.objects.get(name=auth.get_username())
        new_user.access_token_key = request.session.get('access_token_key')
        new_user.access_token_secret= request.session.get('access_token_secret')
    else:
        new_user = User(name=auth.get_username(),
                        access_token_key=request.session.get('access_token_key'),
                        access_token_secret=request.session.get('access_token_secret'),
                       )
    new_user.save()
    request.session['session_user'] = new_user
    return HttpResponseRedirect(reverse("index"))

def get_home_timeline(request):
    auth = setOAauth(request)
    api = tweepy.API(auth_handler=auth)
    home_timeline = api.home_timeline()
    return direct_to_template(request, "skz2.html", {"tweets":home_timeline})
