# Generated by Django 5.0.1 on 2024-06-09 14:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('news', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=models.SET(None), to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='postcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.category'),
        ),
        migrations.AddField(
            model_name='postcategory',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.post'),
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(related_name='post', through='news.PostCategory', to='news.category', verbose_name='Категория'),
        ),
    ]
