from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="details")
    bio = models.TextField(max_length=500, blank=True)
    nickname = models.CharField(max_length=30, default="0000000")


def create_user_profile(sender, instance, created, **kwargs):
    """Autocreate Profile whenever a new user is created
    
    Docs: https://docs.djangoproject.com/en/3.1/ref/signals/#django.db.models.signals.post_save

    :param sender: the model class that triggers this
    :param instance: the created instance after saving
    :param created: true/false if the instance was created
    """
    if created:
        UserProfile.objects.create(user=instance)


signals.post_save.connect(
    create_user_profile,
    sender=User,
    weak=False,
    dispatch_uid="models.create_user_profile",
)
