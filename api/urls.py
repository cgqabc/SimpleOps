#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    url(r'^assets/$', views.assets_list),
    url(r'^project/$', views.project_list),
    url(r'^project/(?P<id>[0-9]+)/$', views.project_detail),
    url(r'^service/$', views.service_list),
    url(r'^service/(?P<id>[0-9]+)/$', views.service_detail),
    url(r'^assets/(?P<id>[0-9]+)/$', views.assets_detail),

]

urlpatterns = format_suffix_patterns(urlpatterns)