# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Ansible_Inventory)
admin.site.register(Ansible_Server)
admin.site.register(Ansible_Group)
admin.site.register(Ansible_CallBack_Model_Result)
admin.site.register(Ansible_CallBack_PlayBook_Result)
admin.site.register(Log_Ansible_Model)
admin.site.register(Log_Ansible_Playbook)
admin.site.register(Global_Config)
admin.site.register(Ansible_Script)
admin.site.register(Ansible_Playbook)