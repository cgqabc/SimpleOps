"""SimpleOps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, include
from accounts import user, role, permission


urlpatterns = [
    # url(r'^$', user.user_list, name='accounts'),
    # url(r'^login/$', user.login, name='login'),
    # url(r'^logout/$', user.logout, name='logout'),
    url(r'^list/$', user.user_list, name='user_list'),
    url(r'^add/$', user.user_add, name='user_add'),
    url(r'^delete/(?P<ids>\d+)/$', user.user_del, name='user_del'),
    url(r'^edit/(?P<ids>\d+)/$', user.user_edit, name='user_edit'),
    url(r'^reset/password/(?P<ids>\d+)/$', user.reset_password, name='reset_password'),
    url(r'^change/password/$', user.change_password, name='change_password'),
    url(r'^role/add/$', role.role_add, name='role_add'),
    url(r'^role/list/$', role.role_list, name='role_list'),
    url(r'^role/edit/(?P<ids>\d+)/$', role.role_edit, name='role_edit'),
    url(r'^role/delete/(?P<ids>\d+)/$', role.role_del, name='role_del'),
    url(r'^permission/deny/$', permission.permission_deny, name='permission_deny'),
    url(r'^permission/add/$', permission.permission_add, name='permission_add'),
    url(r'^permission/list/$', permission.permission_list, name='permission_list'),
    url(r'^permission/edit/(?P<ids>\d+)/$', permission.permission_edit, name='permission_edit'),
    url(r'^permission/delete/(?P<ids>\d+)/$', permission.permission_del, name='permission_del'),
]
