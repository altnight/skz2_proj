#from yonda.models import *
from django.contrib import admin

from skz2.models import User
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'access_token_key', 'access_token_secret', 'ctime',)
    readonly_fields = ('ctime','access_token_key', 'access_token_secret')

#class UrlAdmin(admin.ModelAdmin):
    #list_display = ('url', 'title', 'user', 'ctime','atime',)
    #readonly_fields = ('ctime', 'atime')

admin.site.register(User, UserAdmin)
#admin.site.register(Url, UrlAdmin)
