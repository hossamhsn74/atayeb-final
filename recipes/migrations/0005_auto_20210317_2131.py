# Generated by Django 3.0.13 on 2021-03-17 21:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20210317_2059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='image',
        ),
        migrations.RemoveField(
            model_name='ingredientcategory',
            name='image',
        ),
    ]
