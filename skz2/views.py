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

#from yonda.forms import *
#from yonda.models import *
#from yonda.tools import use_username_or_masuda

def index(request):
    """トップページ"""
    #loginしてるとき
    if request.method == "GET":
        return direct_to_template(request, "index.html", {"form":UrlPostForm()})
    if request.method == "POST":
        form = UrlPostForm(request.POST)
        if not form.is_valid():
            return HttpResponseRedirect(reverse('index'))
        user = use_username_or_masuda(request)
        Url.post_url(form.cleaned_data["url"], user)
        return HttpResponseRedirect(reverse('index'))

