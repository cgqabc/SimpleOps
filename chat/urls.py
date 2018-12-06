#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^ajax/$', views.ajax),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),

]