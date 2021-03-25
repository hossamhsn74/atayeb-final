# Generated by Django 3.0.13 on 2021-03-24 23:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0005_auto_20210323_2126'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='عنوان المنشور')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاريخ الإضافة')),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=None, default='static/recipes/images/assets/default_no_pic.png', force_format='PNG', keep_meta=True, null=True, quality=100, size=[750, 750], upload_to='recipes_pics', verbose_name='الصورة')),
                ('body', models.TextField(blank=True, null=True, verbose_name='المحتوي')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Profile', verbose_name='الكاتب')),
            ],
            options={
                'verbose_name_plural': 'المنشورات',
                'ordering': ('date_created',),
            },
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='فئة المنشور')),
            ],
            options={
                'verbose_name_plural': 'فئات المنشور',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='اسم العلامة')),
            ],
            options={
                'verbose_name_plural': 'العلامات',
            },
        ),
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(verbose_name='نص التعليق')),
                ('comment_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاريخ التعليق')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_author', to='user.Profile', verbose_name='الكاتب')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_post', to='blog.Post', verbose_name='المنشور')),
            ],
            options={
                'verbose_name_plural': 'التعليقات',
                'ordering': ('-comment_date',),
            },
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.PostCategory', verbose_name='فئة المنشور'),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag'),
        ),
    ]
