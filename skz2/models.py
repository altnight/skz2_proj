from django.db import models
#-*- coding: utf-8 -*-

class User(models.Model):
    name = models.CharField(u"ユーザー固有のID", max_length=10)
    ctime = models.DateTimeField(u'登録日時',auto_now_add=True, editable=False)
    atime = models.DateTimeField(u'更新日時',auto_now=True, editable=False)
    access_token_key = models.CharField(u'access_token_key',max_length=255)
    access_token_secret = models.CharField(u'access_token_secret',max_length=255)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'User'

#class Tweet(models.Model):
    #user_id = models.CharField(u"ユーザー固有のID", max_length=10)
    #name = models.CharField(u"name", max_length=30)
    #screen_name = models.CharField(u"screen_name", max_length=20)
    #text = models.CharField(u"本文", max_length=140)
    #in_reply_to = models.CharField(u"in_reply_to", max_length=30)
    #since_id = models.CharField(u"since_id", max_length=30)
    #favorited = models.BooleanField(u"fav")
    #created_at = models.CharField(u'作成日時', max_length=40)

    #def __unicode__(self):
        #return "%s:%s" % (self.screen_name, self.text)

    #class Meta:
        #db_table = 'Tweet'
