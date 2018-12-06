#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Permissions(models.Model):
    name = models.CharField(max_length=64, unique=True)
    url = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        return self.name


class RolueGroups(models.Model):
    name = models.CharField(max_length=64, unique=True)
    permission = models.ManyToManyField(Permissions)

    def __unicode__(self):
        return self.name

class User_info(AbstractUser):

    role = models.ForeignKey(RolueGroups,on_delete=models.CASCADE,blank=True,null=True)
    c_time = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.username
    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class LogUserStatus(models.Model):
    user = models.OneToOneField(User_info,on_delete=models.CASCADE,related_name='loguser')