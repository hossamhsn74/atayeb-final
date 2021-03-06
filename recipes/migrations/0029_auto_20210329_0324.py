# Generated by Django 3.0.13 on 2021-03-29 03:24

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0028_auto_20210329_0323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format='PNG', keep_meta=True, quality=100, size=[750, 750], upload_to='recipe_images/', verbose_name='الصورة'),
        ),
    ]
