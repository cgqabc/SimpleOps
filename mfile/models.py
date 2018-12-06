#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models

class LogFileOps(models.Model):
    opstype = models.CharField(max_length=20,choices=(('up','分发'),('down','下载')),
                               verbose_name="操作类型",default='up')
    srcfile = models.CharField(max_length=100,verbose_name="源文件路径",blank=True,null=True,default=None)
    filepath = models.CharField(max_length=100,verbose_name="目标文件路径",blank=True,null=True,default=None)
    server = models.CharField(max_length=100,verbose_name="目标服务器")
    content = models.CharField(max_length=100,blank=True,null=True,verbose_name="备注")
    user = models.CharField(max_length=50, verbose_name='执行者', blank=True,null=True,default=None)
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='执行时间')

    def __unicode__(self):
        return "{}:{}".format(self.opstype,self.create_time)

    class Meta:
        verbose_name = "文件操作记录表"