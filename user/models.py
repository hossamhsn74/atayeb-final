from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django_resized import ResizedImageField


class Profile(models.Model):
    image = ResizedImageField(
        default='static/recipes/images/assets/default_profile_picture.png', upload_to='profile_images')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=250, blank=True,
                           default="Contributer User")

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwarg):
    if kwarg['created']:
        Profile.objects.create(user=kwarg['instance'])


post_save.connect(create_profile, sender=User)
