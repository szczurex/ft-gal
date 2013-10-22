from django.db import models
from profiles.models import Profile
from gallery.models import Submission


class Favourite(models.Model):
    profile = models.ForeignKey(Profile)
    submission = models.ForeignKey(Submission)
    
    date_created = models.DateTimeField(verbose_name='Creation date', auto_now_add=True)
    
    class Meta:
        ordering = ['-date_created']