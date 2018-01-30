from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True)
    followers = models.ManyToManyField(User, related_name='user_followers')

    def __str__(self):
        return self.user.first_name


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Tweets(models.Model):
    created_by = models.ForeignKey('auth.User')
    text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)

    def __str__(self):
        return self.text
