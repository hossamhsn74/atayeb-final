from PIL import Image
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


def get_resized_image(obj, req_width=300, req_height=300):
    img = Image.open(obj.image.path)
    if img.width > req_width or img.height > req_height:
        output_size = (req_width, req_height)
        img.thumbnail(output_size)
    return img


class Profile(models.Model):
    image = models.ImageField(default='static/recipes/images/assets/default_profile_picture.png', upload_to='profile_pics')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} profile.'.format(self.user.username)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = get_resized_image(self, req_width=300, req_height=300)
        img.save(self.image.path)


def create_profile(sender, **kwarg):
    if kwarg['created']:
        Profile.objects.create(user=kwarg['instance'])


post_save.connect(create_profile, sender=User)
