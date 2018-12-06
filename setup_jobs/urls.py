#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^job_add/$', views.job_add,name="job_add"),
    url(r'^job_edit/(?P<job_id>[0-9]+)/$', views.job_edit,name="job_edit"),
    url(r'^job_del/(?P<job_id>[0-9]+)/$', views.job_del,name="job_del"),
    url(r'^cron_add/$', views.cron_add, name="cron_add"),
    url(r'^cron_edit/(?P<cron_id>[0-9]+)/$', views.cron_edit, name="cron_edit"),
    url(r'^interval_add/$', views.interval_add, name="interval_add"),
    url(r'^interval_edit/(?P<interval_id>[0-9]+)/$', views.interval_edit, name="interval_edit"),
    url(r'^solar_add/$', views.solar_add, name="solar_add"),
    url(r'^solar_edit/(?P<solar_id>[0-9]+)/$', views.solar_edit, name="solar_edit"),
    url(r'^task_result/$', views.task_result, name="task_result"),
    url(r'^task_result_del/(?P<result_id>[0-9]+)/$', views.task_result_del, name="task_result_del"),


]