# Generated by Django 3.0.13 on 2021-03-25 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0021_auto_20210324_1610'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('date_created',), 'verbose_name_plural': 'الوصفات'},
        ),
    ]