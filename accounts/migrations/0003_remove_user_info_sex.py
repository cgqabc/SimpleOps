# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-09-30 06:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20180831_1432'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_info',
            name='sex',
        ),
    ]
