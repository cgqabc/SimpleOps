# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-11-30 02:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email_Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.CharField(max_length=100, verbose_name='\u90e8\u7f72\u7ad9\u70b9')),
                ('host', models.CharField(max_length=100, verbose_name='\u90ae\u4ef6\u53d1\u9001\u670d\u52a1\u5668')),
                ('port', models.SmallIntegerField(verbose_name='\u90ae\u4ef6\u53d1\u9001\u670d\u52a1\u5668\u7aef\u53e3')),
                ('user', models.CharField(max_length=100, verbose_name='\u53d1\u9001\u7528\u6237\u8d26\u6237')),
                ('passwd', models.CharField(max_length=100, verbose_name='\u53d1\u9001\u7528\u6237\u5bc6\u7801')),
                ('subject', models.CharField(default='[OPS]', max_length=100, verbose_name='\u53d1\u9001\u90ae\u4ef6\u4e3b\u9898\u6807\u8bc6')),
                ('cc_user', models.TextField(blank=True, null=True, verbose_name='\u6284\u9001\u7528\u6237\u5217\u8868')),
            ],
            options={
                'verbose_name': '\u90ae\u4ef6\u914d\u7f6e\u8868',
                'verbose_name_plural': '\u90ae\u4ef6\u914d\u7f6e\u8868',
            },
        ),
    ]
