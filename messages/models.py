from django.db import models


class TaskedMail(models.Model):
    subject         = models.CharField(verbose_name='Mail subject', max_length=150)
    destination     = models.EmailField(verbose_name='Mail destination', max_length=75)
    message         = models.CharField(verbose_name='Mail content', max_length=2000)
    success         = models.BooleanField(verbose_name='Mail sent status', default=False)
    date_created    = models.DateTimeField(verbose_name='Mail creation date', auto_now_add=True)
    
    
#class Notification