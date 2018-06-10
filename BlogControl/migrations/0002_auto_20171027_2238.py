# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-27 22:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogControl', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ('date_created',)},
        ),
        migrations.AddField(
            model_name='blog',
            name='date_created',
            field=models.DateTimeField(auto_created=True, default=datetime.datetime(2017, 10, 27, 22, 38, 47, 298332)),
        ),
    ]