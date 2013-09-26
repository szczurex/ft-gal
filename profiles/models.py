from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
import base64, hashlib, random
from datetime import datetime, timedelta



class Profile(AbstractUser):
    avatar = models.ImageField(verbose_name="Avatar", upload_to='avatars')
   # last_ip = TODO
   
   
class ActivationCode(models.Model):
    profile         = models.ForeignKey(Profile)
    key             = models.CharField(verbose_name="Key", max_length=32)
    expiration_date = models.DateTimeField(verbose_name="Expiration date")
    activated       = models.BooleanField(verbose_name="Key used", default=False)
    
    def set_up(self, profile):
        key                     = base64.b64encode(hashlib.sha256(str(random.getrandbits(256))).digest(),
                                                   random.choice(['rA','aZ','gQ','hH','hG','aR','DD'])).rstrip('==')
        self.key                = key[0:32]
        self.expiration_date    = datetime.now()+timedelta(days=2)
        self.profile            = profile
        
        return self
    
    
class ProfileWatch(models.Model):
    profile = models.ForeignKey(Profile, related_name="profile_source") # profile watching
    target  = models.ForeignKey(Profile, related_name="profile_target") # profile who is being watched
    
    journal = models.BooleanField(verbose_name="Journals", default=True)
    gallery = models.BooleanField(verbose_name="Submissions", default=True)
    scraps  = models.BooleanField(verbose_name="Scraps", default=True)
    
    date_created = models.DateTimeField(verbose_name="Date created", auto_now_add=True)

# NO - THIS IS WRONG.    
#     class Meta:
#         unique_together = ("profile", "target")
        

"""
    Check - if you're not watching anything, delete the watch instance,
    you're not a watcher.
"""
def check_empty_watch(sender, instance, **kwargs):
    if not instance.journal and not instance.gallery and not instance.scraps:
        instance.delete()

post_save.connect(check_empty_watch, ProfileWatch)