"""SimpleOps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin

import accounts.urls
from . import views
import accounts.user
import cmdb.urls
import chat.urls
import setup_jobs.urls
import deploy.urls
import api.urls
import delivery.urls

urlpatterns = [
    url(r'^admin/', admin.site.urls,name="admin"),
    url(r'^login/',accounts.user.login,name='login'),
    url(r'^user/', include('accounts.urls')),
    url(r'^logout/', accounts.user.logout, name='logout'),
    url(r'^cmdb/',include('cmdb.urls')),
    url(r'^chat/', include('chat.urls')),
    url(r'^setup_jobs/',include('setup_jobs.urls')),
    url(r'^deploy/',include('deploy.urls')),
    url(r'^$',views.index,name='index'),
    url(r'^mfile/', include('mfile.urls')),
    url(r'^elfinder/', include('elfinder.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^delivery/', include('delivery.urls')),
    url(r'^config/$', views.config,name='config'),
    # url(r'^websocket/(?P<userid>[0-9]+)$',views.websocket_tst,name='websocket'),
]
handler400 = "SimpleOps.views.bad_request"
handler404 = "SimpleOps.views.page_not_found"
handler403 = "SimpleOps.views.page_not_permission"
handler500 = "SimpleOps.views.internl_error"