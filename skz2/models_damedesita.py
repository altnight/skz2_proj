from django.db import models
#import pickle

# Create your models here.
class Tweet(models.Model):
    #def __init__(self, status):
        #self.status = status
    status = models.CharField(u"Status", max_length=5000)
    #status = models.TextField(u"Status")

    #def __unicode__(self):
        #return self.status

    class Meta:
        db_table = 'Tweet'
