# Generated by Django 3.0.13 on 2021-05-04 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20210502_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='العلامات'),
        ),
    ]
