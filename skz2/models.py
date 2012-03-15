from django.db import models
#-*- coding: utf-8 -*-
import datetime

class User(models.Model):
    name = models.CharField(u"ユーザー固有のID", max_length=10)
    ctime = models.DateTimeField(u'登録日時',auto_now_add=True, editable=False)
    atime = models.DateTimeField(u'更新日時',auto_now=True, editable=False)
    access_token = models.CharField(u'access_token',max_length=255)
    access_token_secret = models.CharField(u'access_token_secret',max_length=255)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'User'

class Tweet(models.Model):
    user_id = models.CharField(u"ユーザー固有のID", max_length=10)
    status_id = models.CharField(u"status", max_length=30)
    name = models.CharField(u"name", max_length=30)
    screen_name = models.CharField(u"screen_name", max_length=20)
    user_image_url = models.CharField(u"user_image", max_length=200)
    text = models.CharField(u"本文", max_length=140)
    source = models.CharField(u"source", max_length=30)
    source_url = models.CharField(u"source_url", max_length=50, blank=True, null=True)
    in_reply_to_status_id = models.CharField(u"in_reply_to", max_length=40, blank=True, null=True)
    #since_id = models.CharField(u"since_id", max_length=30)
    favorited = models.BooleanField(u"fav")
    created_at = models.CharField(u'作成日時', max_length=40)
    protected = models.BooleanField(u"protect")
    ctime = models.DateTimeField(u'登録日時',auto_now_add=True, editable=False)

    def __unicode__(self):
        return "%s:%s" % (self.screen_name, self.text)

    class Meta:
        db_table = 'Tweet'

    @classmethod
    def saveTweet(cls, tweet, text):

        #Webだったら
        if not tweet.source_url:
            source_url = "http://twitter.com/"
        else:
            source_url = tweet.source_url

        t = cls(user_id = tweet.user.id_str,
                status_id = tweet.id_str,
                name = tweet.user.name,
                screen_name = tweet.user.screen_name,
                user_image_url = tweet.user.profile_image_url,
                text = text,
                in_reply_to_status_id = tweet.in_reply_to_status_id,
                favorited = tweet.favorited,
                created_at = tweet.created_at + datetime.timedelta(0, 3600*9),
                protected = tweet.user.protected,
                source = tweet.source,
                source_url = source_url,
                 )
        t.save()
