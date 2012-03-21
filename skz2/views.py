#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
#from django.shortcuts import get_object_or_404
from django.utils import simplejson as json

from skz2.models import User, Tweet, Lists
from skz2.mappers import TweetMapper, ListsMapper, RateLimitMapper

import tweepy
from see import see

from config import TwitterOAuth
from skz2.tools import setOAuth, expandURL

CONSUMER_KEY = TwitterOAuth.consumer_key
CONSUMER_SECRET = TwitterOAuth.consumer_secret
CALLBACK_URL = TwitterOAuth.callback_url

def index(request):
    if request.session.get('session_user'):
        return direct_to_template(request, "skz2.html",{})
    else:
        return direct_to_template(request, 'index.html',{})

def delete_session(request):
    if request.session.get('session_user'):
        del request.session['session_user']
    if request.session.get('home_timeline_since_id'):
        del request.session['home_timeline_since_id']
    if request.session.get('mentions_since_id'):
        del request.session['mentions_since_id']
    #if request.session.get('list_timeline_since_id'):
        #del request.session['list_timeline_since_id']
    return HttpResponseRedirect(reverse('index'))

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

def update_status(request):
    auth = setOAuth(request)
    api = tweepy.API(auth_handler=auth)
    try:
        api.update_status(request.GET.get('q'))
    except Exception:
        print Exception

def get_home_timeline(request):

    auth = setOAuth(request)
    api = tweepy.API(auth_handler=auth)
    home_timeline = api.home_timeline(count = 200, since_id=request.session.get('home_timeline_since_id'), include_entities=True)
    home_timeline.reverse()
    for tweet in home_timeline:

        if tweet == home_timeline[0]:
            request.session['home_timeline_since_id'] = tweet.id_str

        #公式RT対応
        old_tweet = None
        if hasattr(tweet, 'retweeted_status'):
            old_tweet = tweet
            tweet = tweet.retweeted_status

        text = expandURL(tweet)
        Tweet.saveTweet(request, tweet, text, old_tweet)

    home_timeline_query = Tweet.objects.filter(user=request.session.get('session_user')).order_by('-ctime')[:200]

    home_timeline_dict = [TweetMapper(obj).as_dict() for obj in home_timeline_query]
    home_timeline_json = json.dumps(home_timeline_dict)
    return HttpResponse(home_timeline_json, mimetype='application/json')

def get_lists(request):
    auth = setOAuth(request)
    api = tweepy.API(auth_handler=auth)
    lists = api.lists()
    lists.reverse()

    #一度既存のリスト一覧を削除
    Lists.objects.filter(user=request.session.get('session_user')).delete()
    for li in lists:
        list_members = [member.screen_name for member in li.members()]
        l = Lists(name = li.name,
                  full_name = li.full_name,
                  members = list_members,
                  user = request.session.get('session_user'),
                )
        l.save()
    lists_query = Lists.objects.filter(user=request.session.get('session_user'))
    lists_dict = [ListsMapper(obj).as_dict() for obj in lists_query]
    lists_json = json.dumps(lists_dict)
    return HttpResponse(lists_json, mimetype='application/json')

def get_mentions(request):
    auth = setOAuth(request)
    api = tweepy.API(auth_handler=auth)
    mentions = api.mentions(count = 50, since_id=request.session.get('mentions_since_id'), include_entities=True)
    mentions.reverse()
    for tweet in mentions:

        if tweet == mentions[0]:
            request.session['memtions_since_id'] = tweet.id_str

        text = expandURL(tweet)
        Tweet.saveTweet(request, tweet, text)

    mentions_query = Tweet.objects.filter(user=request.session.get('session_user')).order_by('-ctime')[:50]

    mentions_dict = [TweetMapper(obj).as_dict() for obj in mentions_query]
    mentions_json = json.dumps(mentions_dict)
    return HttpResponse(mentions_json, mimetype='application/json')
    #return direct_to_template(request, "skz2.html", {"tweets":mentions_query})

def get_direct_messages(request):
    auth = setOAuth(request)
    api = tweepy.API(auth_handler=auth)
    direct_messages = api.direct_messages(count = 30, include_entities=True)
    direct_messages.reverse()
    for tweet in direct_messages:

        text = expandURL(tweet)
        Tweet.saveDMTweet(request, tweet, text)

    direct_messages_query = Tweet.objects.filter(user=request.session.get('session_user')).order_by('-ctime')[:30]

    direct_messages_dict = [TweetMapper(obj).as_dict() for obj in direct_messages_query]
    direct_messages_json = json.dumps(direct_messages_dict)
    return HttpResponse(direct_messages_json, mimetype='application/json')
    #return direct_to_template(request, "skz2.html", {"tweets":direct_messages_query})

def get_sent_direct_messages(request):
    auth = setOAuth(request)
    api = tweepy.API(auth_handler=auth)
    sent_direct_messages = api.sent_direct_messages(count = 30, include_entities=True)
    sent_direct_messages.reverse()
    for tweet in sent_direct_messages:

        text = expandURL(tweet)
        Tweet.saveDMTweet(request, tweet, text)

    sent_direct_messages_query = Tweet.objects.filter(user=request.session.get('session_user')).order_by('-ctime')[:30]

    sent_direct_messages_dict = [TweetMapper(obj).as_dict() for obj in sent_direct_messages_query]
    sent_direct_messages_json = json.dumps(sent_direct_messages_dict)
    return HttpResponse(sent_direct_messages_json, mimetype='application/json')
    #return direct_to_template(request, "skz2.html", {"tweets":sent_direct_messages_query})

def get_list_timeline(request, list_owner, list_name):

    auth = setOAuth(request)
    api = tweepy.API(auth_handler=auth)
    #import pdb;pdb.set_trace()
    rts = request.GET.get('rts')
    list_timeline = api.list_timeline(owner=list_owner, slug=list_name, count = 200, include_entities=True, include_rts=rts)
    list_timeline.reverse()
    for tweet in list_timeline:

        #if tweet == list_timeline[0]:
            #request.session['list_timeline_since_id'] = tweet.id_str

        #公式RT対応
        old_tweet = None
        if hasattr(tweet, 'retweeted_status'):
            old_tweet = tweet
            tweet = tweet.retweeted_status

        text = expandURL(tweet)
        Tweet.saveTweet(request, tweet, text, old_tweet)

    list_timeline_query = Tweet.objects.filter(user=request.session.get('session_user')).order_by('-ctime')[:200]

    list_timeline_dict = [TweetMapper(obj).as_dict() for obj in list_timeline_query]
    list_timeline_json = json.dumps(list_timeline_dict)
    return HttpResponse(list_timeline_json, mimetype='application/json')
    #return direct_to_template(request, "skz2.html", {"tweets":list_timeline_query})

def get_api_limit(request):
    auth = setOAuth(request)
    api = tweepy.API(auth_handler=auth)
    api_limit = api.rate_limit_status()

    remaining = api_limit['remaining_hits']
    hourly_limit = api_limit['hourly_limit']
    reset_time = api_limit['reset_time']

    api_limit_dict = {"remaining":remaining, "hourly_limit":hourly_limit, "reset_time":reset_time}
    api_limit_json= json.dumps(api_limit_dict)
    return HttpResponse(api_limit_json, mimetype='application/json')
