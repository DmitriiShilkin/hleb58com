# Generated by Django 5.0.1 on 2024-01-06 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(blank=True, max_length=254, null=True, verbose_name='Описание'),
        ),
    ]