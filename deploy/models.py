# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from accounts.models import User_info
from cmdb.models import Assets
# Create your models here.

class Ansible_Inventory(models.Model):
    name = models.CharField(unique=True,max_length=100, verbose_name="名称")
    desc = models.CharField(max_length=200,verbose_name="功能描述")
    create_user = models.ForeignKey(User_info,related_name="ansible_inventory",
                                    on_delete=models.CASCADE, verbose_name="创建人")
    create_time = models.DateField(auto_now_add=True,blank=True,null=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "动态资产表"
        verbose_name_plural = "动态资产表"


class Ansible_Group(models.Model):
    inventory = models.ForeignKey(Ansible_Inventory,related_name="inventory_group",
                                  on_delete=models.CASCADE, verbose_name="资产名称")
    group = models.CharField(max_length=100,unique=True,verbose_name="组名")
    ext_vars = models.TextField(verbose_name='组外部变量', blank=True, null=True)

    def __unicode__(self):
        return self.group

    class Meta:
        verbose_name = "动态资产分组表"
        verbose_name_plural = "动态资产分组表"


class Ansible_Server(models.Model):
    group = models.ForeignKey(Ansible_Group,related_name="inventory_server",
                                  on_delete=models.CASCADE, verbose_name="资产组")
    # server = models.CharField(max_length=100,verbose_name="服务器")
    server = models.SmallIntegerField(verbose_name="服务器",default=None)


    def __unicode__(self):
        # return self.server.manage_ip
        return str(self.id)
    class Meta:
        unique_together = ["group","server"]
        verbose_name = "组内成员表"
        verbose_name_plural = "组内成员表"


class Global_Config(models.Model):
    ansible_model = models.SmallIntegerField(verbose_name='是否开启ansible模块操作记录',blank=True,null=True)
    ansible_playbook = models.SmallIntegerField(verbose_name='是否开启ansible剧本操作记录',blank=True,null=True)
    cron = models.SmallIntegerField(verbose_name='是否开启计划任务操作记录',blank=True,null=True)
    project = models.SmallIntegerField(verbose_name='是否开启项目操作记录',blank=True,null=True)
    assets = models.SmallIntegerField(verbose_name='是否开启资产操作记录',blank=True,null=True)
    server = models.SmallIntegerField(verbose_name='是否开启服务器命令记录',blank=True,null=True)
    email = models.SmallIntegerField(verbose_name='是否开启邮件通知',blank=True,null=True)
    webssh = models.SmallIntegerField(verbose_name='是否开启WebSSH',blank=True,null=True)
    sql = models.SmallIntegerField(verbose_name='是否开启SQL更新通知',blank=True,null=True)
    class Meta:
        verbose_name = "ansible日志配置表"
        verbose_name_plural = "ansible日志配置表"

class Email_Config(models.Model):
    site = models.CharField(max_length=100,verbose_name='部署站点')
    host = models.CharField(max_length=100,verbose_name='邮件发送服务器')
    port = models.SmallIntegerField(verbose_name='邮件发送服务器端口')
    user = models.CharField(max_length=100,verbose_name='发送用户账户')
    passwd = models.CharField(max_length=100,verbose_name='发送用户密码')
    subject = models.CharField(max_length=100,verbose_name='发送邮件主题标识',default=u'[OPS]')
    cc_user = models.TextField(verbose_name='抄送用户列表',blank=True,null=True)
    class Meta:
        verbose_name = "邮件配置表"
        verbose_name_plural = "邮件配置表"
class Ansible_CallBack_Model_Result(models.Model):
    logId = models.ForeignKey('Log_Ansible_Model',related_name="ansible_model_log")
    content = models.TextField(verbose_name='输出内容', blank=True, null=True)
    def __unicode__(self):
        return str(self.logId)

class Ansible_CallBack_PlayBook_Result(models.Model):
    logId = models.ForeignKey('Log_Ansible_Playbook',related_name="ansible_playbook_log")
    content = models.TextField(verbose_name='输出内容', blank=True, null=True)
    def __unicode__(self):
        return str(self.logId)

class Log_Ansible_Model(models.Model):
    ans_user = models.CharField(max_length=50,verbose_name='使用用户',default=None)
    ans_model = models.CharField(max_length=100,verbose_name='模块名称',default=None)
    ans_args = models.CharField(max_length=500,blank=True,null=True,verbose_name='模块参数',default=None)
    ans_server = models.TextField(verbose_name='服务器',default=None)
    create_time = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name='执行时间')
    def __unicode__(self):
        return "{0}|{1}".format(self.ans_model,self.create_time)

    class Meta:
        verbose_name = 'Ansible模块执行记录表'
        verbose_name_plural = 'Ansible模块执行记录表'

class Log_Ansible_Playbook(models.Model):
    ans_id = models.IntegerField(verbose_name='id',blank=True,null=True,default=None)
    ans_user = models.CharField(max_length=50,verbose_name='使用用户',default=None)
    ans_name = models.CharField(max_length=100,verbose_name='模块名称',default=None)
    ans_content = models.CharField(max_length=100,default=None)
    ans_server = models.TextField(verbose_name='服务器',default=None)
    create_time = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name='执行时间')
    def __unicode__(self):
        return "{0}|{1}".format(self.ans_name,self.create_time)
    class Meta:
        verbose_name = 'Ansible剧本操作记录表'
        verbose_name_plural = 'Ansible剧本操作记录表'

class Ansible_Script(models.Model):
    script_name = models.CharField(max_length=50,verbose_name='脚本名称',unique=True)
    script_uuid = models.CharField(max_length=50,verbose_name='唯一id',blank=True,null=True)
    script_server = models.TextField(verbose_name='目标机器',blank=True,null=True)
    script_file = models.FileField(upload_to = './script/',verbose_name='脚本路径')
    script_args = models.TextField(blank=True,null=True,verbose_name='脚本参数')
    script_service = models.SmallIntegerField(verbose_name='授权业务',blank=True,null=True)
    script_group = models.SmallIntegerField(verbose_name='授权组',blank=True,null=True)
    script_type = models.CharField(max_length=50,verbose_name='脚本类型',blank=True,null=True)

    def __unicode__(self):
        return self.script_name
    class Meta:

        verbose_name = 'Ansible脚本配置表'
        verbose_name_plural = 'Ansible脚本配置表'


class Ansible_Playbook(models.Model):
    type = (
        ('service', u'service'),
        ('group', u'group'),
        ('custom', u'custom'),
    )
    playbook_name = models.CharField(max_length=50, verbose_name='剧本名称', unique=True)
    playbook_desc = models.CharField(max_length=200, verbose_name='功能描述', blank=True, null=True)
    playbook_vars = models.TextField(verbose_name='模块参数', blank=True, null=True)
    playbook_uuid = models.CharField(max_length=50, verbose_name='唯一id')
    playbook_server_model = models.CharField(choices=type, verbose_name='服务器选择类型', max_length=10, blank=True, null=True)
    playbook_server_value = models.SmallIntegerField(verbose_name='服务器选择类型值', blank=True, null=True)
    playbook_file = models.FileField(upload_to='./playbook/', verbose_name='剧本路径')
    playbook_auth_group = models.SmallIntegerField(verbose_name='授权组', blank=True, null=True)
    playbook_auth_user = models.SmallIntegerField(verbose_name='授权用户', blank=True, null=True, )
    playbook_type = models.SmallIntegerField(verbose_name='剧本类型', blank=True, null=True, default=0)
    def __unicode__(self):
        return self.playbook_name
    class Meta:

        verbose_name = 'Ansible剧本配置表'
        verbose_name_plural = 'Ansible剧本配置表'
