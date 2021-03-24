# Generated by Django 3.0.13 on 2021-03-24 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FaqQuestionBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=128, verbose_name='العنوان')),
                ('answer', models.TextField(max_length=128, verbose_name='التفاصيل')),
            ],
            options={
                'verbose_name_plural': 'الاسئلة المكررة',
            },
        ),
        migrations.CreateModel(
            name='FaqShortBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=128, verbose_name='العنوان')),
                ('answer', models.TextField(max_length=128, verbose_name='التفاصيل')),
            ],
            options={
                'verbose_name_plural': 'اقسام الاسئلة المكررة',
            },
        ),
    ]