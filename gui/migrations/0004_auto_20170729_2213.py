# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-29 22:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gui', '0003_data_file_name_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='stats',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='data',
            name='times',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]