from django.conf.urls import url

import views

urlpatterns = [
    url(r'^list/', views.delivery_list, name='delivery_list'),
    url(r'^add/$', views.delivery_add, name='delivery_add'),
    url(r'^edit/(?P<pid>[0-9]+)/$', views.delivery_edit, name='delivery_edit'),
    url(r'^run/(?P<pid>[0-9]+)/$', views.delivery_run, name='delivery_run'),
    url(r'^init/(?P<pid>[0-9]+)/$', views.delivery_init, name='delivery_init'),
    url(r'^result/(?P<pid>[0-9]+)/$', views.delivery_result, name='delivery_result'),
    url(r'^version/(?P<pid>[0-9]+)/$', views.delivery_version, name='delivery_version'),
    url(r'^del/(?P<id>[0-9]+)/$', views.delivery_del, name='delivery_del'),
    url(r'^log/$', views.delivery_log, name='delivery_log'),

]
