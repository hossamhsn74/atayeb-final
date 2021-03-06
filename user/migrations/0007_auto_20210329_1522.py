# Generated by Django 3.0.13 on 2021-03-29 15:22

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20210329_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, default=None, force_format='PNG', keep_meta=True, quality=100, size=[750, 750], upload_to='profile_images/'),
        ),
    ]
