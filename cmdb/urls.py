from django.conf.urls import url

import views

app_name = "cmdb"
urlpatterns = [
    url(r'^report/', views.report, name='report'),
    url(r'^assets_info/$', views.assets_info, name='assets_info'),
    url(r'^project/', views.project, name='project'),
    url(r'^new_asset_permission/$', views.new_asset_permission, name='new_asset_permission'),
    url(r'^new_asset_del/(?P<asset_id>[0-9]+)/$', views.new_asset_del, name='new_asset_del'),
    url(r'^new_asset_allow/(?P<asset_id>[0-9]+)/$', views.new_asset_allow, name='new_asset_allow'),
    url(r'^business_unit/$', views.business_unit, name='business_unit'),
    url(r'^business_add/$', views.business_add, name='business_add'),
    url(r'^business_edit/(?P<bus_id>[0-9]+)/$', views.business_edit, name='business_edit'),
    url(r'^business_del/(?P<bus_id>[0-9]+)/$', views.business_del, name='business_del'),
    url(r'^project_list/$', views.project_list, name='project_list'),
    url(r'^project_add/$', views.project_add, name='project_add'),
    url(r'^project_edit/(?P<bus_id>[0-9]+)/$', views.project_edit, name='project_edit'),
    url(r'^project_del/(?P<bus_id>[0-9]+)/$', views.project_del, name='project_del'),
    url(r'^detail/(?P<asset_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^asset_server_query/$', views.assets_server_query, name='assets_server_query'),
    url(r'^asset_edit/(?P<asset_id>[0-9]+)/$', views.asset_edit, name='asset_edit'),
    url(r'^asset_del/(?P<asset_id>[0-9]+)/$', views.asset_del, name='asset_del'),
    url(r'^asset_add/', views.asset_add, name='asset_add'),
    url(r'^asset_batch_import/', views.asset_batch_import, name='asset_batch_import'),
]
