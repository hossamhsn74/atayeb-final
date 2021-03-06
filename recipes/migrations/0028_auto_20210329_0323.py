# Generated by Django 3.0.13 on 2021-03-29 03:23

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0027_auto_20210328_2312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipecategory',
            name='description',
        ),
        migrations.RemoveField(
            model_name='recipecategory',
            name='image',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, default=None, force_format='PNG', keep_meta=True, quality=100, size=[750, 750], upload_to='recipe_images/', verbose_name='الصورة'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(to='recipes.Tag', verbose_name='العلامات'),
        ),
    ]
