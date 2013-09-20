from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from profiles.models import Profile

class TaskedMail(models.Model):
    subject         = models.CharField(verbose_name='Mail subject', max_length=150)
    destination     = models.EmailField(verbose_name='Mail destination', max_length=75)
    message         = models.CharField(verbose_name='Mail content', max_length=2000)
    success         = models.BooleanField(verbose_name='Mail sent status', default=False)
    date_created    = models.DateTimeField(verbose_name='Mail creation date', auto_now_add=True)
    

class Notification(models.Model):
    profile = models.ForeignKey(Profile, related_name="notif_profile")
    author = models.ForeignKey(Profile, related_name="notif_author")
    
    #submission/journal/comment/favourite/watch GenericKey
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    
    date_created = models.DateTimeField(verbose_name='Creation date', auto_now_add=True)
    
    class Meta:
        unique_together = ("profile", "author")