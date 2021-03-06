from django.db import models
from profiles.models import Profile

# TODO: file verification
from gallery.validators import THUMB_VALIDATOR, FILE_VALIDATOR, MIMES_IMAGE
from PIL import Image


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

FILE_TYPES = (
    (FILE_TYPE_IMAGE, 'Image'),
    (FILE_TYPE_WRITING, 'Text'),
    (FILE_TYPE_MUSIC, 'Music'),
    (FILE_TYPE_FLASH, 'Flash'),
)


class Submission(models.Model):
    profile = models.ForeignKey(Profile)
    # meta
    title = models.CharField(verbose_name="Title", max_length=200)
    description = models.CharField(verbose_name="Description", max_length=5000)
    rating = models.SmallIntegerField(verbose_name="Rating", choices=RATING)
    # file
    file = models.FileField(verbose_name="File uploaded", max_length=200, upload_to="submissions")
    thumb = models.ImageField(verbose_name="Custom thumbnail", max_length=200, upload_to="submissions_thumbs",
                              null=True, blank=True)
    file_type = models.SmallIntegerField(verbose_name="Submission type", choices=FILE_TYPES)
    scrap = models.BooleanField(verbose_name='Scrap', default=False)
    # internals
    file_mime = models.CharField(verbose_name="Mimetype", max_length=5000,
                                 null=True, blank=True)
    date_created = models.DateTimeField(verbose_name="Date created", auto_now_add=True)
    date_edited = models.DateTimeField(verbose_name="Date modified", auto_now=True)
    hidden = models.BooleanField(verbose_name='Hidden', default=False)
    deleted = models.BooleanField(verbose_name='Submission deleted?', default=False)
    
    # TODO: pageviews, ratings, faving
    
    class Meta:
        ordering = ['-date_created']
        
    @property
    def file_width(self):
        if self.file_mime in MIMES_IMAGE:
            im = Image.open(self.file)
            width, height = im.size
            return width
        return None


# consider django-mptt
class Submission_Comment(models.Model):
    profile = models.ForeignKey(Profile) #author
    submission = models.ForeignKey(Submission)
    comment = models.ForeignKey("gallery.Submission_Comment", null=True, blank=True) #reply to a comment
    
    content = models.CharField(verbose_name="", max_length=5000)
    
    date_created = models.DateTimeField(verbose_name="Date created", auto_now_add=True)
    deleted = models.BooleanField(verbose_name='Comment deleted?', default=False)
    
    #TODO: banning, blocking, etc
    
    class Meta:
        ordering = ['-date_created']