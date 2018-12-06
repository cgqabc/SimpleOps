# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-11-19 08:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0003_auto_20181116_1503'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ansible_CallBack_Model_Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True, verbose_name='\u8f93\u51fa\u5185\u5bb9')),
            ],
        ),
        migrations.CreateModel(
            name='Ansible_CallBack_PlayBook_Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True, verbose_name='\u8f93\u51fa\u5185\u5bb9')),
            ],
        ),
        migrations.CreateModel(
            name='Global_Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ansible_model', models.SmallIntegerField(blank=True, null=True, verbose_name='\u662f\u5426\u5f00\u542fansible\u6a21\u5757\u64cd\u4f5c\u8bb0\u5f55')),
                ('ansible_playbook', models.SmallIntegerField(blank=True, null=True, verbose_name='\u662f\u5426\u5f00\u542fansible\u5267\u672c\u64cd\u4f5c\u8bb0\u5f55')),
                ('cron', models.SmallIntegerField(blank=True, null=True, verbose_name='\u662f\u5426\u5f00\u542f\u8ba1\u5212\u4efb\u52a1\u64cd\u4f5c\u8bb0\u5f55')),
                ('project', models.SmallIntegerField(blank=True, null=True, verbose_name='\u662f\u5426\u5f00\u542f\u9879\u76ee\u64cd\u4f5c\u8bb0\u5f55')),
                ('assets', models.SmallIntegerField(blank=True, null=True, verbose_name='\u662f\u5426\u5f00\u542f\u8d44\u4ea7\u64cd\u4f5c\u8bb0\u5f55')),
                ('server', models.SmallIntegerField(blank=True, null=True, verbose_name='\u662f\u5426\u5f00\u542f\u670d\u52a1\u5668\u547d\u4ee4\u8bb0\u5f55')),
                ('email', models.SmallIntegerField(blank=True, null=True, verbose_name='\u662f\u5426\u5f00\u542f\u90ae\u4ef6\u901a\u77e5')),
                ('webssh', models.SmallIntegerField(blank=True, null=True, verbose_name='\u662f\u5426\u5f00\u542fWebSSH')),
                ('sql', models.SmallIntegerField(blank=True, null=True, verbose_name='\u662f\u5426\u5f00\u542fSQL\u66f4\u65b0\u901a\u77e5')),
            ],
            options={
                'verbose_name': 'ansible\u65e5\u5fd7\u914d\u7f6e\u8868',
                'verbose_name_plural': 'ansible\u65e5\u5fd7\u914d\u7f6e\u8868',
            },
        ),
        migrations.CreateModel(
            name='Log_Ansible_Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ans_user', models.CharField(default=None, max_length=50, verbose_name='\u4f7f\u7528\u7528\u6237')),
                ('ans_model', models.CharField(default=None, max_length=100, verbose_name='\u6a21\u5757\u540d\u79f0')),
                ('ans_args', models.CharField(blank=True, default=None, max_length=500, null=True, verbose_name='\u6a21\u5757\u53c2\u6570')),
                ('ans_server', models.TextField(default=None, verbose_name='\u670d\u52a1\u5668')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u6267\u884c\u65f6\u95f4')),
            ],
            options={
                'db_table': 'opsmanage_log_ansible_model',
                'verbose_name': 'Ansible\u6a21\u5757\u6267\u884c\u8bb0\u5f55\u8868',
                'verbose_name_plural': 'Ansible\u6a21\u5757\u6267\u884c\u8bb0\u5f55\u8868',
                'permissions': (('can_read_log_ansible_model', '\u8bfb\u53d6Ansible\u6a21\u5757\u6267\u884c\u8bb0\u5f55\u6743\u9650'), ('can_change_log_ansible_model', '\u66f4\u6539Ansible\u6a21\u5757\u6267\u884c\u8bb0\u5f55\u6743\u9650'), ('can_add_log_ansible_model', '\u6dfb\u52a0Ansible\u6a21\u5757\u6267\u884c\u8bb0\u5f55\u6743\u9650'), ('can_delete_log_ansible_model', '\u5220\u9664Ansible\u6a21\u5757\u6267\u884c\u8bb0\u5f55\u6743\u9650')),
            },
        ),
        migrations.CreateModel(
            name='Log_Ansible_Playbook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ans_id', models.IntegerField(blank=True, default=None, null=True, verbose_name='id')),
                ('ans_user', models.CharField(default=None, max_length=50, verbose_name='\u4f7f\u7528\u7528\u6237')),
                ('ans_name', models.CharField(default=None, max_length=100, verbose_name='\u6a21\u5757\u540d\u79f0')),
                ('ans_content', models.CharField(default=None, max_length=100)),
                ('ans_server', models.TextField(default=None, verbose_name='\u670d\u52a1\u5668')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u6267\u884c\u65f6\u95f4')),
            ],
            options={
                'db_table': 'opsmanage_log_ansible_playbook',
                'verbose_name': 'Ansible\u5267\u672c\u64cd\u4f5c\u8bb0\u5f55\u8868',
                'verbose_name_plural': 'Ansible\u5267\u672c\u64cd\u4f5c\u8bb0\u5f55\u8868',
                'permissions': (('can_read_log_ansible_playbook', '\u8bfb\u53d6Ansible\u5267\u672c\u6267\u884c\u8bb0\u5f55\u6743\u9650'), ('can_change_log_ansible_playbook', '\u66f4\u6539Ansible\u5267\u672c\u6267\u884c\u8bb0\u5f55\u6743\u9650'), ('can_add_log_ansible_playbook', '\u6dfb\u52a0Ansible\u5267\u672c\u6267\u884c\u8bb0\u5f55\u6743\u9650'), ('can_delete_log_ansible_playbook', '\u5220\u9664Ansible\u5267\u672c\u6267\u884c\u8bb0\u5f55\u6743\u9650')),
            },
        ),
        migrations.AlterModelOptions(
            name='ansible_group',
            options={'verbose_name': '\u52a8\u6001\u8d44\u4ea7\u5206\u7ec4\u8868', 'verbose_name_plural': '\u52a8\u6001\u8d44\u4ea7\u5206\u7ec4\u8868'},
        ),
        migrations.AlterModelOptions(
            name='ansible_server',
            options={'verbose_name': '\u7ec4\u5185\u6210\u5458\u8868', 'verbose_name_plural': '\u7ec4\u5185\u6210\u5458\u8868'},
        ),
        migrations.AddField(
            model_name='ansible_callback_playbook_result',
            name='logId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deploy.Log_Ansible_Playbook'),
        ),
        migrations.AddField(
            model_name='ansible_callback_model_result',
            name='logId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deploy.Log_Ansible_Model'),
        ),
    ]
