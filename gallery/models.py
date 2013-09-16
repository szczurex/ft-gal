from django.db import models
from profiles.models import Profile

# TODO: file verification

RATING_GENERAL  = 1
RATING_MATURE   = 2
RATING_ADULT    = 3

RATING = (
    (RATING_GENERAL, 'General'),
    (RATING_MATURE, 'Mature'),
    (RATING_ADULT, 'Adult')
)

FILE_TYPE_IMAGE     = 1
FILE_TYPE_WRITING   = 2
FILE_TYPE_MUSIC     = 3
FILE_TYPE_FLASH     = 4

class Submission(models.Model):
    profile = models.ForeignKey(Profile)
    # meta
    title = models.CharField(verbose_name="Title", max_length=200)
    description = models.CharField(verbose_name="Description", max_length=5000)
    rating = models.SmallIntegerField(verbose_name="Rating", choices=RATING)
    # file
    file = models.FileField(verbose_name="File uploaded", max_length=200, upload_to="submissions")
    thumb = models.ImageField(verbose_name="Custom thumbnail", max_length=200, upload_to="submissions_thumbs")
    #file_type = models.CharField(verbose_name="Submission type", choices=)
    # internals
    date_created = models.DateTimeField(verbose_name="Date created", auto_now_add=True)
    date_edited = models.DateTimeField(verbose_name="Date modified", auto_now=True)
    hidden = models.BooleanField(verbose_name='Hidden', default=False)
    deleted = models.BooleanField(verbose_name='Journal deleted?', default=False)