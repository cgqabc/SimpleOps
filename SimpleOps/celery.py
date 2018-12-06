#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
import os
from celery import Celery
from django.conf import settings
# from  django_celery_beat import models

os.environ.setdefault("DJANGO_SETTINGS_MODULE","SimpleOps.settings")
app=Celery('simpleops')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.  ( namespace='CELERY')
app.config_from_object('django.conf:settings',namespace='CELERY')

# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))