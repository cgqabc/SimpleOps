# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-11-27 08:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mfile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='logfileops',
            name='srcfile',
            field=models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name=b'\xe6\xba\x90\xe6\x96\x87\xe4\xbb\xb6\xe8\xb7\xaf\xe5\xbe\x84'),
        ),
        migrations.AlterField(
            model_name='logfileops',
            name='filepath',
            field=models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name=b'\xe7\x9b\xae\xe6\xa0\x87\xe6\x96\x87\xe4\xbb\xb6\xe8\xb7\xaf\xe5\xbe\x84'),
        ),
        migrations.AlterField(
            model_name='logfileops',
            name='user',
            field=models.CharField(blank=True, default=None, max_length=50, null=True, verbose_name=b'\xe6\x89\xa7\xe8\xa1\x8c\xe8\x80\x85'),
        ),
    ]
