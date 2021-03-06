# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-11-01 07:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0003_server_asset_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='CPU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu_model', models.CharField(blank=True, max_length=128, null=True, verbose_name='CPU\u578b\u53f7')),
                ('cpu_number', models.PositiveSmallIntegerField(default=1, verbose_name='\u7269\u7406CPU\u4e2a\u6570')),
                ('cpu_core', models.PositiveSmallIntegerField(default=1, verbose_name='CPU\u6838\u6570')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cmdb.Assets')),
            ],
            options={
                'verbose_name': 'CPU',
                'verbose_name_plural': 'CPU',
            },
        ),
        migrations.RemoveField(
            model_name='server_asset',
            name='cpu_core',
        ),
        migrations.RemoveField(
            model_name='server_asset',
            name='cpu_model',
        ),
        migrations.RemoveField(
            model_name='server_asset',
            name='cpu_number',
        ),
    ]
