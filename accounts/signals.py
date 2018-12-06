#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth import user_logged_in,user_logged_out
from django.dispatch import receiver
from .models import LogUserStatus
from channels import Group
import json
@receiver(user_logged_in)
def loginuser(sender,**kwargs):
    LogUserStatus.objects.get_or_create(user=kwargs.get('user'))
    Group('users').send({
        'text': json.dumps({
            'username': kwargs.get('user').username,
            'is_logged_in': True
       })
    })
@receiver(user_logged_out)
def logoutuser(sender,**kwargs):
    LogUserStatus.objects.filter(user=kwargs.get('user')).delete()
    Group('users').send({
        'text': json.dumps({
            'username': kwargs.get('user').username,
            'is_logged_in': False
        })
    })