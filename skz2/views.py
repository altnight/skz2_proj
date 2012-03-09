# Create your views here.
#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
#from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
#from django.contrib.csrf.middleware import csrf_exempt
#from django.shortcuts import get_object_or_404
#from django.core.mail import send_mail
import tweepy
from see import see

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
CALLBACK_URL = ''

def index(request):
    if request.session.get('session_user'):
        return direct_to_template(request, "skz2.html",{'skz2':skz2})
    else:
        return direct_to_template(request, 'index.html',{})

def login(request):
    if request.method == "GET":
        return direct_to_template(request, 'login.html',{'form':LoginForm()})
    if request.method == "POST":
        form = LoginForm(request.POST)
        if not form.is_valid():
            return HttpResponseRedirect(reverse('index'))
        #存在しないユーザーならindexに戻す
        if not User.objects.filter(name=request.POST.get('name')).count():
            return HttpResponseRedirect(reverse('index'))
        request.session['session_user'] = request.POST.get('name')
        return HttpResponseRedirect(reverse('index'))

def logout(request):
    if request.session.get('session_user'):
        del request.session['session_user']
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

    request.session['key'] = auth.access_token.key
    request.session['secret'] = auth.access_token.secret

    if User.objects.filter(access_token_key=request.session.get('key')).count():
        signuped_user = User.objects.get(access_token_key=request.session.get('key'))
        request.session['session_user'] = signuped_user.name
        return HttpResponseRedirect(reverse('index'))
    return HttpResponseRedirect(reverse('create_profile'))
