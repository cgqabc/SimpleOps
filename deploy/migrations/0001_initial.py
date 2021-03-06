# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-11-29 08:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            name='Ansible_Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(max_length=100, unique=True, verbose_name='\u7ec4\u540d')),
                ('ext_vars', models.TextField(blank=True, null=True, verbose_name='\u7ec4\u5916\u90e8\u53d8\u91cf')),
            ],
            options={
                'verbose_name': '\u52a8\u6001\u8d44\u4ea7\u5206\u7ec4\u8868',
                'verbose_name_plural': '\u52a8\u6001\u8d44\u4ea7\u5206\u7ec4\u8868',
            },
        ),
        migrations.CreateModel(
            name='Ansible_Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='\u540d\u79f0')),
                ('desc', models.CharField(max_length=200, verbose_name='\u529f\u80fd\u63cf\u8ff0')),
                ('create_time', models.DateField(auto_now_add=True, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('create_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ansible_inventory', to=settings.AUTH_USER_MODEL, verbose_name='\u521b\u5efa\u4eba')),
            ],
            options={
                'verbose_name': '\u52a8\u6001\u8d44\u4ea7\u8868',
                'verbose_name_plural': '\u52a8\u6001\u8d44\u4ea7\u8868',
            },
        ),
        migrations.CreateModel(
            name='Ansible_Playbook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playbook_name', models.CharField(max_length=50, unique=True, verbose_name='\u5267\u672c\u540d\u79f0')),
                ('playbook_desc', models.CharField(blank=True, max_length=200, null=True, verbose_name='\u529f\u80fd\u63cf\u8ff0')),
                ('playbook_vars', models.TextField(blank=True, null=True, verbose_name='\u6a21\u5757\u53c2\u6570')),
                ('playbook_uuid', models.CharField(max_length=50, verbose_name='\u552f\u4e00id')),
                ('playbook_server_model', models.CharField(blank=True, choices=[('service', 'service'), ('group', 'group'), ('custom', 'custom')], max_length=10, null=True, verbose_name='\u670d\u52a1\u5668\u9009\u62e9\u7c7b\u578b')),
                ('playbook_server_value', models.SmallIntegerField(blank=True, null=True, verbose_name='\u670d\u52a1\u5668\u9009\u62e9\u7c7b\u578b\u503c')),
                ('playbook_file', models.FileField(upload_to='./playbook/', verbose_name='\u5267\u672c\u8def\u5f84')),
                ('playbook_auth_group', models.SmallIntegerField(blank=True, null=True, verbose_name='\u6388\u6743\u7ec4')),
                ('playbook_auth_user', models.SmallIntegerField(blank=True, null=True, verbose_name='\u6388\u6743\u7528\u6237')),
                ('playbook_type', models.SmallIntegerField(blank=True, default=0, null=True, verbose_name='\u5267\u672c\u7c7b\u578b')),
            ],
            options={
                'verbose_name': 'Ansible\u5267\u672c\u914d\u7f6e\u8868',
                'verbose_name_plural': 'Ansible\u5267\u672c\u914d\u7f6e\u8868',
            },
        ),
        migrations.CreateModel(
            name='Ansible_Script',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('script_name', models.CharField(max_length=50, unique=True, verbose_name='\u811a\u672c\u540d\u79f0')),
                ('script_uuid', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u552f\u4e00id')),
                ('script_server', models.TextField(blank=True, null=True, verbose_name='\u76ee\u6807\u673a\u5668')),
                ('script_file', models.FileField(upload_to='./script/', verbose_name='\u811a\u672c\u8def\u5f84')),
                ('script_args', models.TextField(blank=True, null=True, verbose_name='\u811a\u672c\u53c2\u6570')),
                ('script_service', models.SmallIntegerField(blank=True, null=True, verbose_name='\u6388\u6743\u4e1a\u52a1')),
                ('script_group', models.SmallIntegerField(blank=True, null=True, verbose_name='\u6388\u6743\u7ec4')),
                ('script_type', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u811a\u672c\u7c7b\u578b')),
            ],
            options={
                'verbose_name': 'Ansible\u811a\u672c\u914d\u7f6e\u8868',
                'verbose_name_plural': 'Ansible\u811a\u672c\u914d\u7f6e\u8868',
            },
        ),
        migrations.CreateModel(
            name='Ansible_Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server', models.SmallIntegerField(default=None, verbose_name='\u670d\u52a1\u5668')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory_server', to='deploy.Ansible_Group', verbose_name='\u8d44\u4ea7\u7ec4')),
            ],
            options={
                'verbose_name': '\u7ec4\u5185\u6210\u5458\u8868',
                'verbose_name_plural': '\u7ec4\u5185\u6210\u5458\u8868',
            },
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
                'verbose_name': 'Ansible\u6a21\u5757\u6267\u884c\u8bb0\u5f55\u8868',
                'verbose_name_plural': 'Ansible\u6a21\u5757\u6267\u884c\u8bb0\u5f55\u8868',
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
                'verbose_name': 'Ansible\u5267\u672c\u64cd\u4f5c\u8bb0\u5f55\u8868',
                'verbose_name_plural': 'Ansible\u5267\u672c\u64cd\u4f5c\u8bb0\u5f55\u8868',
            },
        ),
        migrations.AddField(
            model_name='ansible_group',
            name='inventory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory_group', to='deploy.Ansible_Inventory', verbose_name='\u8d44\u4ea7\u540d\u79f0'),
        ),
        migrations.AddField(
            model_name='ansible_callback_playbook_result',
            name='logId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ansible_playbook_log', to='deploy.Log_Ansible_Playbook'),
        ),
        migrations.AddField(
            model_name='ansible_callback_model_result',
            name='logId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ansible_model_log', to='deploy.Log_Ansible_Model'),
        ),
        migrations.AlterUniqueTogether(
            name='ansible_server',
            unique_together=set([('group', 'server')]),
        ),
    ]
