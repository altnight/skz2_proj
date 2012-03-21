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
    url(r'^update_status$', 'update_status', name='update_status'),
    url(r'^get_home_timeline$', 'get_home_timeline', name='get_home_timeline'),
    url(r'^get_mentions$', 'get_mentions', name='get_mentions'),
    url(r'^get_direct_messages$', 'get_direct_messages', name='get_direct_messages'),
    url(r'^get_sent_direct_messages$', 'get_sent_direct_messages', name='get_sent_direct_messages'),
    url(r'^get_lists$', 'get_lists', name='get_lists'),
    url(r'^get_list_timeline/(?P<list_owner>\w+)/(?P<list_name>\w+)/$', 'get_list_timeline', name='get_list_timeline'),
    url(r'^get_api_limit$', 'get_api_limit', name='get_api_limit'),
)

