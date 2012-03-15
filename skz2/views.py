#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
#from django.shortcuts import get_object_or_404

from skz2.models import User, Tweet

import tweepy
from see import see
import datetime
import re
from requests import get

from config import TwitterOAuth
from skz2.tools import setOAuth
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

    if User.objects.filter(name = auth.get_username()).count():
        new_user = User.objects.get(name=auth.get_username())
        new_user.access_token = auth.access_token.key
        new_user.access_token_secret = auth.access_token.secret
    else:
        new_user = User(name = auth.get_username(),
                        access_token = auth.access_token.key,
                        access_token_secret = auth.access_token.secret,
                       )
    new_user.save()
    request.session['session_user'] = new_user
    return HttpResponseRedirect(reverse("index"))

def get_home_timeline(request):
    #import pdb;pdb.set_trace()
    auth = setOAuth(request)
    api = tweepy.API(auth_handler=auth)
    home_timeline = api.home_timeline(count = 100,since_id = request.session.get('since_id'), include_entities=True)
    for i in home_timeline:
        text = i.text

        for url in i.entities['urls']:
            if url is None:
                continue
            elif re.search(r't\.co', text):
                for ii in i.entities['urls']:
                    text = re.sub(r'https?://t\.co/[\w_\.\/]+', ii['expanded_url'], text)


        #if i == home_timeline[0]:
            #request.session['since_id'] = i.id_str
        user =  re.search(r'(@[\w]+)', text)
        if user is None:
            pass
        else:
            pass
            #print user.group(1)
            #text = text.replace(user.group(1), '<a href="http://twitter.com/#!/"+i.user.screen_name>user.group(1)</a>')
            #text = re.sub(r'https?://[\w_\.\/]+', '<a href="https://twitter.com/#!/">user.group(1)</a>' text)

        hashtag =  re.search(r'(#[\w一-龠ぁ-んァ-ヴー]+)', text)
        if hashtag is None:
            pass
        else:
            pass
            #print hashtag.group(1)
            #text = '<a href="https://twitter.com/#!/search/"'+hashtag.group(1)+ '>'+hashtag.group(1) +"</a>"
            #text = "<a href=%s>%s</a>" % ("https://twitter.com/#!/search/", hashtag.group(1))
        t = Tweet(user_id = i.user.id_str,
                  status_id = i.id_str,
                  name = i.user.name,
                  screen_name = i.user.screen_name,
                  text = text,
                  in_reply_to_status_id = i.in_reply_to_status_id,
                  favorited = i.favorited,
                  created_at = i.created_at + datetime.timedelta(0, 3600*9),
                  protected = i.user.protected,
                  source = i.source,
                  source_url = i.source_url,
                 )
        t.save()
    tm = Tweet.objects.all().order_by('-created_at')[:100]
    return direct_to_template(request, "skz2.html", {"tweets":tm})
