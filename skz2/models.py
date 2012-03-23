from django.db import models
#-*- coding: utf-8 -*-
import datetime

class User(models.Model):
    name = models.CharField(u"ユーザー固有のID", max_length=10)
    ctime = models.DateTimeField(u'登録日時',auto_now_add=True, editable=False)
    atime = models.DateTimeField(u'更新日時',auto_now=True, editable=False)
    access_token = models.CharField(u'access_token',max_length=255)
    access_token_secret = models.CharField(u'access_token_secret',max_length=255)
    #activated = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'User'

class Tweet(models.Model):
    userid = models.CharField(u"ユーザー固有のID", max_length=10)
    status_id = models.CharField(u"status", max_length=30)
    name = models.CharField(u"name", max_length=30)
    screen_name = models.CharField(u"screen_name", max_length=20)
    user_image_url = models.CharField(u"user_image", max_length=200)
    text = models.CharField(u"本文", max_length=140)
    source = models.CharField(u"source", max_length=30)
    source_url = models.CharField(u"source_url", max_length=50)
    #in_reply_to_status_id = models.CharField(u"in_reply_to", max_length=40, blank=True, null=True)
    favorited = models.BooleanField(u"fav")
    retweeted = models.BooleanField(u"retweet")
    created_at = models.CharField(u'ツイートの作成日時', max_length=40)
    protected = models.BooleanField(u"protect")
    old_tweet_screen_name = models.CharField(u'retweetした人のscreen_name',  max_length=20, blank=True, null=True)
    old_tweet_user_image_url = models.CharField(u'retweetした人のuser_image', max_length=200, blank=True, null=True)
    retweeted_count = models.CharField(u'retweet_count', max_length=10, blank=True, null=True)
    ctime = models.DateTimeField(u'登録日時',auto_now_add=True, editable=False)
    user = models.ForeignKey(User, verbose_name=u'ユーザー')

    def __unicode__(self):
        return "%s:%s" % (self.screen_name, self.text)

    class Meta:
        db_table = 'Tweet'

    @classmethod
    def saveTweet(cls, request, tweet, text, old_tweet=None):

        #Webだったら
        if not tweet.source_url:
            source_url = "http://twitter.com/"
        else:
            source_url = tweet.source_url

        #公式RTされたなら
        if old_tweet:
            t = cls(userid = tweet.user.id_str,
                status_id = tweet.id_str,
                name = tweet.user.name,
                screen_name = tweet.user.screen_name,
                user_image_url = tweet.user.profile_image_url,
                text = text,
                #in_reply_to_status_id = tweet.in_reply_to_status_id,
                favorited = tweet.favorited,
                retweeted = tweet.retweeted,
                created_at = tweet.created_at + datetime.timedelta(0, 3600*9),
                protected = tweet.user.protected,
                source = tweet.source,
                source_url = source_url,
                old_tweet_screen_name = old_tweet.user.screen_name,
                old_tweet_user_image_url = old_tweet.user.profile_image_url,
                retweeted_count = old_tweet.retweet_count,
                user = request.session.get('session_user'),
               )
        else:
            t = cls(userid = tweet.user.id_str,
                status_id = tweet.id_str,
                name = tweet.user.name,
                screen_name = tweet.user.screen_name,
                user_image_url = tweet.user.profile_image_url,
                text = text,
                #in_reply_to_status_id = tweet.in_reply_to_status_id,
                favorited = tweet.favorited,
                retweeted = tweet.retweeted,
                created_at = tweet.created_at + datetime.timedelta(0, 3600*9),
                protected = tweet.user.protected,
                source = tweet.source,
                source_url = source_url,
                user = request.session.get('session_user'),
               )
        t.save()

    @classmethod
    def saveDMTweet(cls, request, tweet, text):
        t = cls(userid = tweet.sender_id,
                status_id = tweet.id_str,
                name = tweet.sender.name,
                screen_name = tweet.sender_screen_name,
                user_image_url = tweet.sender.profile_image_url,
                text = text,
                #in_reply_to_status_id = tweet.id_str,
                created_at = tweet.created_at + datetime.timedelta(0, 3600*9),
                user = request.session.get('session_user'),
               )
        t.save()

class Lists(models.Model):
    name = models.CharField(u"リストの名前", max_length=30)
    full_name = models.CharField(u"リストのフルネーム", max_length=30)
    members = models.CharField(u"リストのフォロー", max_length=1000)
    ctime = models.DateTimeField(u'登録日時',auto_now_add=True, editable=False)
    atime = models.DateTimeField(u'更新日時',auto_now=True, editable=False)
    user = models.ForeignKey(User, verbose_name=u'ユーザー')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'Lists'

#class List(models.Model):
    #list1 = models.CharField(u"リストの名前1", max_length=30)
    #list2 = models.CharField(u"リストの名前2", max_length=30)
    #list3 = models.CharField(u"リストの名前3", max_length=30)
    #list4 = models.CharField(u"リストの名前4", max_length=30)
    #list5 = models.CharField(u"リストの名前5", max_length=30)
    #list6 = models.CharField(u"リストの名前6", max_length=30)
    #list7 = models.CharField(u"リストの名前7", max_length=30)
    #list8 = models.CharField(u"リストの名前8", max_length=30)
    #list9 = models.CharField(u"リストの名前9", max_length=30)
    #list10 = models.CharField(u"リストの名前10", max_length=30)
    #list11 = models.CharField(u"リストの名前11", max_length=30)
    #list12 = models.CharField(u"リストの名前12", max_length=30)
    #list13 = models.CharField(u"リストの名前13", max_length=30)
    #list14 = models.CharField(u"リストの名前14", max_length=30)
    #list15 = models.CharField(u"リストの名前15", max_length=30)
    #list16 = models.CharField(u"リストの名前16", max_length=30)
    #list17 = models.CharField(u"リストの名前17", max_length=30)
    #list18 = models.CharField(u"リストの名前18", max_length=30)
    #list19 = models.CharField(u"リストの名前19", max_length=30)
    #list20 = models.CharField(u"リストの名前20", max_length=30)
    #atime = models.DateTimeField(u'更新日時',auto_now=True, editable=False)
    #user = models.ForeignKey(User, verbose_name=u'ユーザー')

    #def __unicode__(self):
        #return self.list1

    #class Meta:
        #db_table = 'List'
