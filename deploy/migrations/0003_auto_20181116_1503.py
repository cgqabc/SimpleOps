# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-11-16 07:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0002_auto_20181116_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ansible_server',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asset_server', to='cmdb.Assets', verbose_name='\u670d\u52a1\u5668'),
        ),
    ]