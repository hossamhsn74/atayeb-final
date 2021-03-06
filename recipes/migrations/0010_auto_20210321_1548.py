# Generated by Django 3.0.13 on 2021-03-21 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_auto_20210318_1321'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name_plural': 'العلامات'},
        ),
        migrations.AlterField(
            model_name='recipecategory',
            name='image',
            field=models.ImageField(blank=True, default='static/recipes/images/assets/default_no_pic.png', null=True, upload_to='recipes_pics', verbose_name='الصورة'),
        ),
    ]
