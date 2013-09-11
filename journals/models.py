from django.db import models
from profiles.models import Profile

class Journal(models.Model):
    profile = models.ForeignKey(Profile)
    title = models.CharField(verbose_name="Title", max_length=200)
    content = models.CharField(verbose_name="Content", max_length=5000)
    date_created = models.DateTimeField(verbose_name="Date created", auto_now_add=True)
    date_edited = models.DateTimeField(verbose_name="Date modified", auto_now=True)
    hidden = models.BooleanField(verbose_name='Hidden', default=False)
    deleted = models.BooleanField(verbose_name='Journal deleted?', default=False)