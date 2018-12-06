# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Project_Config)
admin.site.register(Log_Project_Config)
admin.site.register(Project_Number)