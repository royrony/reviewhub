# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-30 14:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]