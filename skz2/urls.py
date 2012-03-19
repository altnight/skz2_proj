#-*- coding:utf-8 -*-
#from fav.models import *
from django.contrib import admin
from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('skz2.views',
    url(r'^$', 'index', name='index'),
    url(r'^delete_session$', 'delete_session', name='delete_session'),
    url(r'^get_oauth$', 'get_oauth', name='get_oauth'),
    url(r'^callback$', 'callback', name='callback'),
    url(r'^get_home_timeline$', 'get_home_timeline', name='get_home_timeline'),
    url(r'^get_lists$', 'get_lists', name='get_lists'),
)

