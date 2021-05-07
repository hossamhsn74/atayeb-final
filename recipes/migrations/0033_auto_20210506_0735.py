# Generated by Django 3.0.13 on 2021-05-06 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0032_auto_20210504_0436'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipeingredient',
            name='unit',
            field=models.CharField(default=None, max_length=255, verbose_name='وحدة القياس'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='quantity',
            field=models.CharField(max_length=255, verbose_name='الكمية'),
        ),
    ]