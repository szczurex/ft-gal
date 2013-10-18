from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from profiles.models import Profile
from django.db.models.signals import post_save

class TaskedMail(models.Model):
    subject         = models.CharField(verbose_name='Mail subject', max_length=150)
    destination     = models.EmailField(verbose_name='Mail destination', max_length=75)
    message         = models.CharField(verbose_name='Mail content', max_length=2000)
    success         = models.BooleanField(verbose_name='Mail sent status', default=False)
    date_created    = models.DateTimeField(verbose_name='Mail creation date', auto_now_add=True)
    

"""
    Notifications should not have a deleted field, would cause a table to grow a bit too much
"""
class Notification(models.Model):
    profile = models.ForeignKey(Profile, related_name="notif_profile")
    author = models.ForeignKey(Profile, related_name="notif_author")
    
    #submission/journal/comment/favourite/watch GenericKey
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    
    date_created = models.DateTimeField(verbose_name='Creation date', auto_now_add=True)
    
    class Meta:
#         unique_together = ("profile", "author")
        ordering = ['-date_created']
        



from profiles.models import ProfileWatch
from journals.models import Journal
from gallery.models import Submission #, Submission_Comment
"""
    Why post_save? pre_save has no ability to check whether the object is modified or created.
"""
def send_notifications(sender, instance, created, **kwargs):
    if created:
        ct = ContentType.objects.get_for_model(sender)
        author = instance.profile
        # all profiles who watch someone, CREATED ONE IS NOT IN HERE YET!
        watchers = ProfileWatch.objects.filter(target=author)
        
        
        # BIG TODO: send notifications based off watch settings. Currently: fuck, all goes.
        for watch in watchers:
            notif = Notification(
                                 profile = watch.profile, #give the notif to the watcher
                                 author = author,
                                 content_object = instance
                                 )
            notif.save()
        
        if sender == ProfileWatch: #final notification
            notif = Notification(
                                 profile = instance.target,
                                 author = author,
                                 content_object = instance
                                 )
            notif.save()

post_save.connect(send_notifications, ProfileWatch)
post_save.connect(send_notifications, Journal)
post_save.connect(send_notifications, Submission)