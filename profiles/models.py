from django.db import models
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
    #TODO: activated - for checking
    
    def set_up(self, profile):
        key                     = base64.b64encode(hashlib.sha256(str(random.getrandbits(256))).digest(),
                                                   random.choice(['rA','aZ','gQ','hH','hG','aR','DD'])).rstrip('==')
        self.key                = key[0:32]
        self.expiration_date    = datetime.now()+timedelta(days=2)
        self.profile            = profile
        
        return self