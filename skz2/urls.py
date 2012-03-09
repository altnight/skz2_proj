#-*- coding:utf-8 -*-
#from fav.models import *
from django.contrib import admin
from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('skz2.views',
    url(r'^$', 'index', name='index'),
    url(r'^login$', 'login', name='login'),
    url(r'^logout$', 'logout', name='logout'),
)

