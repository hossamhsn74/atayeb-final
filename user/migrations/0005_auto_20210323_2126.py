# Generated by Django 3.0.13 on 2021-03-23 21:26

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20210323_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, default='static/recipes/images/assets/default_profile_picture.png', force_format='PNG', keep_meta=True, quality=100, size=[750, 750], upload_to='profile_pics'),
        ),
    ]
