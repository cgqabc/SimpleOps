from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.inventory),

    url(r'^inventory/$', views.inventory),
    url(r'^inventory/add/$', views.inventory_add, name='inventory_add'),
    url(r'^inventory/edit/(?P<in_id>[0-9]+)/$', views.inventory_edit, name='inventory_edit'),
    url(r'^inventory/del/(?P<in_id>[0-9]+)/$', views.inventory_del, name='inventory_del'),
    url(r'^moudel/$', views.moudel_run, name='moudel_run'),
    url(r'^run_result/$', views.get_ansibel_result, name='get_ansibel_result'),
    url(r'^scripts_list/$', views.scripts_list, name='scripts_list'),
    url(r'^scripts_add/$', views.scripts_add, name='scripts_add'),
    url(r'^scripts_run/(?P<s_id>[0-9]+)/$', views.scripts_run, name='scripts_run'),
    url(r'^scripts_del/(?P<s_id>[0-9]+)/$', views.scripts_del, name='scripts_del'),
    url(r'^playbook_list/$', views.playbook_list, name='playbook_list'),
    url(r'^playbook_add/$', views.playbook_add, name='playbook_add'),
    url(r'^playbook_run/(?P<s_id>[0-9]+)/$', views.playbook_run, name='playbook_run'),
    url(r'^playbook_del/(?P<s_id>[0-9]+)/$', views.playbook_del, name='playbook_del'),
    url(r'^ansible_log/$', views.ansible_log, name='ansible_log'),
    url(r'^ansible_log_view/(?P<s_id>[0-9]+)/$', views.ansible_log_view, name='ansible_log_view'),
    url(r'^ansible_log_del/(?P<s_id>[0-9]+)/$', views.ansible_log_del, name='ansible_log_del'),

]
