#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from cmdb.models import Server_asset,Assets
from .models import Ansible_Inventory,Ansible_Group,Ansible_Server


class InventoryForm(forms.Form):
    name = forms.CharField(required=True, label='名称:',
                           error_messages={'required': u'请输入名称', 'invalid': u'名格式错误'},
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': '名称',
                                                         }), )
    desc = forms.CharField(required=True, label='功能描述:',
                          widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'style': 'height:150px;',
                                                        'placeholder': '如：修改用户',
                                                        }), )

class GroupForm(forms.Form):
    inventory =forms.ModelChoiceField(required=False, error_messages={'required': u'选择资产'},
                                       queryset=Ansible_Inventory.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    group = forms.CharField(required=True, label='组名',
                           error_messages={'required': u'请输入组名称', 'invalid': u'名格式错误'},
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': '组名称',
                                                         }), )
    ext_vars = forms.CharField(required=False, label='外部组变量',
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': '组变量,如{"a":"10","b":"20"}',
                                                         }), )
    server = forms.ModelMultipleChoiceField(required=False, error_messages={'required': u'选择主机'},
                                           queryset=Assets.objects.all(),
                                           widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

#
# class ServerForm(forms.Form):
#     group = forms.ModelChoiceField(required=False, error_messages={'required': u'选择组名'},
#                                        queryset=Ansible_Group.objects.all(),
#                                        widget=forms.Select(attrs={'class': 'form-control'}))
#     server = forms.ModelChoiceField(required=False, error_messages={'required': u'选择主机'},
#                                        queryset=Server_asset.objects.all(),
#                                        widget=forms.Select(attrs={'class': 'form-control'}))

class MoudelForm(forms.Form):
    _moudels = ("shell","ping","copy","yum","user","service","file","cron","sync","wget","custom")
    _moudels = zip(_moudels,_moudels)
    inventory = forms.ModelChoiceField(queryset=Ansible_Inventory.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    moudel = forms.ChoiceField(required=True, choices=_moudels, label='选择模块',
                               initial='ping',
                               widget=forms.Select(attrs={'class': 'form-control'}))
    moudel_args = forms.CharField(required=False, label='模块参数',
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': '参数',
                                                         }), )
    _debug = forms.ChoiceField(choices=(('on','开启'),('off','关闭')),label="Debug选项",
                               initial='off',widget=forms.Select(attrs={'class': 'form-control'}))



class ScriptsForm(forms.Form):
    name = forms.CharField(required=True, label='名称',
                           error_messages={'required': u'请输入名称', 'invalid': u'名格式错误'},
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': '如：用户新增',
                                                         }), )
    inventory = forms.ModelChoiceField(queryset=Ansible_Inventory.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))

    scripts_args = forms.CharField(required=False, label='参数',
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': '参数',
                                                         }), )
    _debug = forms.ChoiceField(choices=(('on','开启'),('off','关闭')),label="Debug选项",
                               initial='off',widget=forms.Select(attrs={'class': 'form-control'}))



class PlaybookForm(forms.Form):
    name = forms.CharField(required=True, label='名称',
                           error_messages={'required': u'请输入名称', 'invalid': u'名格式错误'},
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': '如：用户新增',
                                                         }), )
    inventory = forms.ModelChoiceField(queryset=Ansible_Inventory.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))

    playbook_args = forms.CharField(required=False, label='剧本参数',
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': '参数',
                                                         }), )
    playbook_desc = forms.CharField(required=False, label='剧本描述',
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': '作用功能说明',
                                                         }), )
    _debug = forms.ChoiceField(choices=(('on','开启'),('off','关闭')),label="Debug选项",
                               initial='off',widget=forms.Select(attrs={'class': 'form-control'}))