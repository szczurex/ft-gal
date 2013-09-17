from django.db import models
from profiles.models import Profile

# TODO: file verification
from gallery.validators import FileValidator

# Thumbs = 512 kB
# Files = 2048 kB

# audio, images, flash - docs/rtf/odt maybe soonish.
FILE_ALLOWED_MIMES = (
    'audio/mpeg',
    'image/gif',
    'image/jpeg',
    'image/pjpeg',
    'image/png',
    'image/bmp',
    'image/x-bmp',
    'application/x-shockwave-flash',
)
FILE_ALLOWED_EXTENSIONS = (
    'mp3',
    'gif',
    'jpg',
    'png',
    'bmp',
    'swf',
)
THUMB_ALLOWED_MIMES = (
    'image/gif',
    'image/jpeg',
    'image/pjpeg',
    'image/png',
    'image/bmp',
    'image/x-bmp',
)
THUMB_ALLOWED_EXTENSIONS = (
    'gif',
    'jpg',
    'png',
    'bmp',
)

# TODO: pull sizes from settings

THUMB_VALIDATOR = FileValidator(max_size=512*1024,
                                allowed_extensions=THUMB_ALLOWED_EXTENSIONS,
                                allowd_mimetypes=THUMB_ALLOWED_MIMES )
FILE_VALIDATOR = FileValidator(max_size=2*1024*1024,
                               allowed_extensions=FILE_ALLOWED_EXTENSIONS,
                               allowd_mimetypes=FILE_ALLOWED_MIMES )


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
    thumb = models.ImageField(verbose_name="Custom thumbnail", max_length=200, upload_to="submissions_thumbs")
    file_type = models.SmallIntegerField(verbose_name="Submission type", choices=FILE_TYPES)
    # internals
    date_created = models.DateTimeField(verbose_name="Date created", auto_now_add=True)
    date_edited = models.DateTimeField(verbose_name="Date modified", auto_now=True)
    hidden = models.BooleanField(verbose_name='Hidden', default=False)
    deleted = models.BooleanField(verbose_name='Submission deleted?', default=False)
    
    