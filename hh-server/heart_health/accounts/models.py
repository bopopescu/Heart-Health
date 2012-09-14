from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models.signals import post_save
      
class UserProfile(models.Model):
    user = models.OneToOneField('auth.User')
    allow_notifications = models.BooleanField(default=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    preferred_location = models.ForeignKey('survey.Location', null=True)

    class Admin:
        pass
admin.site.register(UserProfile)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

