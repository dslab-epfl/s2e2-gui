# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-30 10:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('display_all_analysis', '0002_auto_20170522_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='curr_project_name',
            field=models.CharField(default='binary', max_length=256),
            preserve_default=False,
        ),
    ]
