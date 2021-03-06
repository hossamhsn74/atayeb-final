# Generated by Django 3.0.13 on 2021-03-24 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20210323_2126'),
        ('recipes', '0017_auto_20210324_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Profile', verbose_name='الكاتب'),
        ),
        migrations.AlterField(
            model_name='recipecomment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='user.Profile', verbose_name='الكاتب'),
        ),
    ]
