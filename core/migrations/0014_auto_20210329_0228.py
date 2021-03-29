# Generated by Django 3.0.13 on 2021-03-29 02:28

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20210329_0226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepagelogo',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default='static/images/atayeb_logo_300.png', force_format='PNG', keep_meta=True, null=True, quality=100, size=[50, 50], upload_to='logo/', verbose_name='الصورة'),
        ),
    ]