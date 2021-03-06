# Generated by Django 3.0.13 on 2021-03-23 21:26

from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20210323_2126'),
        ('recipes', '0013_auto_20210322_0156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default='static/recipes/images/assets/default_no_pic.png', force_format='PNG', keep_meta=True, null=True, quality=100, size=[750, 750], upload_to='recipes_pics', verbose_name='الصورة'),
        ),
        migrations.AlterField(
            model_name='recipecategory',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default='static/recipes/images/assets/default_no_pic.png', force_format='PNG', keep_meta=True, null=True, quality=100, size=[750, 750], upload_to='recipes_pics', verbose_name='الصورة'),
        ),
        migrations.AlterField(
            model_name='recipecomment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='user.Profile', verbose_name='الكاتب'),
        ),
    ]
