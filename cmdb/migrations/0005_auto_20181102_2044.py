# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-11-02 12:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0004_auto_20181101_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server_asset',
            name='line',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='\u7ebf\u8def'),
        ),
        migrations.AlterField(
            model_name='server_asset',
            name='ram_total',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='\u5185\u5b58\u5bb9\u91cf'),
        ),
    ]