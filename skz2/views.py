#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
#from django.shortcuts import get_object_or_404
from django.utils import simplejson as json

from skz2.models import User, Tweet, Lists, RTTweet
from skz2.mappers import TweetMapper, ListsMapper

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
        api.update_status(status=request.GET.get('q'), in_reply_to_status_id=request.GET.get('in_reply_to_status_id'))
    except Exception, e:
        print "発言失敗したっぽい"
        return HttpResponseServerError()
    return HttpResponse()

def get_home_timeline(request):

    auth = setOAuth(request)
    api = tweepy.API(auth_handler=auth)
    try:
        home_timeline = api.home_timeline(count = 200, since_id=request.session.get('home_timeline_since_id'), include_entities=True)
    except Exception, e:
        print "取得失敗したっぽい"
        return HttpResponseServerError()
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

    home_timeline_query = Tweet.objects.filter(user=request.session.get('session_user')).order_by('-ctime')[:100]

    home_timeline_dict = [TweetMapper(obj).as_dict() for obj in home_timeline_query]
    home_timeline_json = json.dumps(home_timeline_dict)
    return HttpResponse(home_timeline_json, mimetype='application/json')

def get_lists(request):
    auth = setOAuth(request)
    api = tweepy.API(auth_handler=auth)
    try:
        lists = api.lists()
    except Exception, e:
        print e
        return HttpResponseServerError()
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
    try:
        mentions = api.mentions(count = 50, since_id=request.session.get('mentions_since_id'), include_entities=True)
    except Exception, e:
        return HttpResponseServerError()
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
    try:
        direct_messages = api.direct_messages(count = 30, include_entities=True)
    except Exception, e:
        return HttpResponseServerError()
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
    try:
        sent_direct_messages = api.sent_direct_messages(count = 30, include_entities=True)
    except Exception, e:
        return HttpResponseServerError()
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
    rts = request.GET.get('rts')
    try:
        list_timeline = api.list_timeline(owner=list_owner, slug=list_name, count = 200, include_entities=True, include_rts=rts)
    except Exception, e:
        return HttpResponseServerError()
    list_timeline.reverse()

    try:
        lis = api.get_list(owner=list_owner, slug=list_name)
    except Exception, e:
        return HttpResponseServerError()
    list_members = [member.screen_name for member in lis.members()]

    for tweet in list_timeline:

        #if tweet == list_timeline[0]:
            #request.session['list_timeline_since_id'] = tweet.id_str

        #公式RT対応
        old_tweet = None
        if hasattr(tweet, 'retweeted_status'):
            old_tweet = tweet
            tweet = tweet.retweeted_status
            #公式RTした人もlist_membersに加える
            list_members.append(tweet.user.screen_name)

        text = expandURL(tweet)
        Tweet.saveTweet(request, tweet, text, old_tweet)

    list_timeline_query = Tweet.objects.filter(user=request.session.get('session_user')).filter(screen_name__in=list_members).order_by('-ctime')[:100]

    list_timeline_dict = [TweetMapper(obj).as_dict() for obj in list_timeline_query]
    list_timeline_json = json.dumps(list_timeline_dict)
    return HttpResponse(list_timeline_json, mimetype='application/json')
    #return direct_to_template(request, "skz2.html.orig", {"tweets":list_timeline_query})

def get_api_limit(request):
    auth = setOAuth(request)
    api = tweepy.API(auth_handler=auth)
    try:
        api_limit = api.rate_limit_status()
    except Exception, e:
        return HttpResponseServerError()

    remaining = api_limit['remaining_hits']
    hourly_limit = api_limit['hourly_limit']
    reset_time = api_limit['reset_time']

    api_limit_dict = {"remaining":remaining, "hourly_limit":hourly_limit, "reset_time":reset_time}
    api_limit_json= json.dumps(api_limit_dict)
    return HttpResponse(api_limit_json, mimetype='application/json')

def toggleFav(request):
    auth = setOAuth(request)
    api = tweepy.API(auth_handler=auth)
    tweet_id = request.GET.get('id')

    #fav状態をチェックする
    try:
        favorited = api.get_status(tweet_id).favorited
    except Exception, e:
        return HttpResponseServerError()

    #まだfavられてない場合
    if not favorited:
        try:
            api.create_favorite(tweet_id)
        except Exception, e:
            return HttpResponseServerError()
        return HttpResponse('{"favorited":"True", "tweet_id":"%s"}' % tweet_id, mimetype='application/json')

    #favられている場合
    else:
        try:
            api.destroy_favorite(tweet_id)
        except Exception, e:
            return HttpResponseServerError()
        return HttpResponse('{"favorited":"False", "tweet_id":"%s"}' % tweet_id, mimetype='application/json')

def toggleRT(request):
    auth = setOAuth(request)
    api = tweepy.API(auth_handler=auth)
    tweet_id = request.GET.get('id')

    #TODO:他のクライアントからRTされた場合のRTの取り消し
    #RT状態をチェックする
    try:
        retweeted= api.get_status(tweet_id).retweeted
    except Exception, e:
        return HttpResponseServerError()

    #まだRTられてない場合
    if not retweeted:
        try:
            Tweet = api.retweet(tweet_id)
        except Exception, e:
            return HttpResponseServerError()
        RTTweet.saveTweet(request, Tweet)
        return HttpResponse('{"retweeted":"True", "tweet_id":"%s"}' % tweet_id, mimetype='application/json')

    #RTされている場合
    else:
        wrapper_tweet = RTTweet.objects.filter(user=request.session.get('session_user')).get(status_id=tweet_id)
        try:
            api.destroy_status(wrapper_tweet.wrapper_status_id)
        except Exception, e:
            return HttpResponseServerError()
        #重複させないためにdeliteする
        RTTweet.objects.filter(user=request.session.get('session_user')).delete()
        return HttpResponse('{"retweeted":"False", "tweet_id":"%s"}' % tweet_id, mimetype='application/json')
