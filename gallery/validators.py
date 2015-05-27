# @brief
# File upload validation from https://gist.github.com/jrosebr1/2140738

# @author dokterbob
# @author jrosebr1

import mimetypes
from os.path import splitext

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat


# Thumbs = 512 kB
# Files = 2048 kB

# audio, images, flash - docs/rtf/odt maybe soonish.

MIMES_AUDIO = ('audio/mpeg',)
EXTNS_AUDIO = ('mp3',)
MIMES_IMAGE = ('image/gif',
               'image/jpeg',
               'image/pjpeg',
               'image/png',
               'image/bmp',
               'image/x-bmp',)
EXTNS_IMAGE = ('gif',
               'jpg',
               'jpeg',
               'png',
               'bmp',)
MIMES_FLASH = ('application/x-shockwave-flash',)
EXTNS_FLASH = ('swf',)

FILE_ALLOWED_MIMES      = MIMES_AUDIO + MIMES_IMAGE + MIMES_FLASH
FILE_ALLOWED_EXTENSIONS = EXTNS_AUDIO + EXTNS_IMAGE + EXTNS_FLASH

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
    'jpeg',
    'png',
    'bmp',
)




class FileValidator(object):
    """
    Validator for files, checking the size, extension and mimetype.

    Initialization parameters:
        allowed_extensions: iterable with allowed file extensions
            ie. ('txt', 'doc')
        allowd_mimetypes: iterable with allowed mimetypes
            ie. ('image/png', )
        min_size: minimum number of bytes allowed
            ie. 100
        max_size: maximum number of bytes allowed
            ie. 24*1024*1024 for 24 MB

    Usage example::

        MyModel(models.Model):
            myfile = FileField(validators=FileValidator(max_size=24*1024*1024), ...)

    """

    extension_message = _("Extension '%(extension)s' not allowed. Allowed extensions are: '%(allowed_extensions)s.'")
    mime_message = _("MIME type '%(mimetype)s' is not valid. Allowed types are: %(allowed_mimetypes)s.")
    min_size_message = _('The current file %(size)s, which is too small. The minumum file size is %(allowed_size)s.')
    max_size_message = _('The current file %(size)s, which is too large. The maximum file size is %(allowed_size)s.')

    def __init__(self, *args, **kwargs):
        self.allowed_extensions = kwargs.pop('allowed_extensions', None)
        self.allowed_mimetypes = kwargs.pop('allowed_mimetypes', None)
        self.min_size = kwargs.pop('min_size', 0)
        self.max_size = kwargs.pop('max_size', None)

    def __call__(self, value):
        """
        Check the extension, content type and file size.
        """

        # Check the extension
        ext = splitext(value.name)[1][1:].lower()
        if self.allowed_extensions and not ext in self.allowed_extensions:
            message = self.extension_message % {
                'extension' : ext,
                'allowed_extensions': ', '.join(self.allowed_extensions)
            }

            raise ValidationError(message)

        # Check the content type
        mimetype = mimetypes.guess_type(value.name)[0]
        if self.allowed_mimetypes and not mimetype in self.allowed_mimetypes:
            message = self.mime_message % {
                'mimetype': mimetype,
                'allowed_mimetypes': ', '.join(self.allowed_mimetypes)
            }

            raise ValidationError(message)

        # Check the file size
        filesize = len(value)
        if self.max_size and filesize > self.max_size:
            message = self.max_size_message % {
                'size': filesizeformat(filesize),
                'allowed_size': filesizeformat(self.max_size)
            }

            raise ValidationError(message)

        elif filesize < self.min_size:
            message = self.min_size_message % {
                'size': filesizeformat(filesize),
                'allowed_size': filesizeformat(self.min_size)
            }

            raise ValidationError(message)
        
        
# TODO: pull sizes/extensions from settings

THUMB_VALIDATOR = FileValidator(max_size=512*1024,
                                allowed_extensions=THUMB_ALLOWED_EXTENSIONS,
                                allowd_mimetypes=THUMB_ALLOWED_MIMES)
FILE_VALIDATOR = FileValidator(max_size=2*1024*1024,
                               allowed_extensions=FILE_ALLOWED_EXTENSIONS,
                               allowd_mimetypes=FILE_ALLOWED_MIMES)