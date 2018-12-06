#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from deploy.models import Ansible_Inventory

class FileUpForm(forms.Form):
    # inventory = forms.ChoiceField(choices=(('0','请选择资产类型'),('1','产品线'),('2','组别'),('3','动态资产表'),('4','自定义')),
    #                               required=True,label='资产类型',
    #                                widget=forms.Select(attrs={'class': 'form-control'}))

    inventory = forms.ModelChoiceField(queryset=Ansible_Inventory.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    filepath = forms.CharField(required=True, label='目标路径',
                           error_messages={'required': u'请输入目标路径', 'invalid': u'格式错误'},
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': '/usr/local/src/',
                                                         }), )
    owner = forms.CharField(required=False, label='文件属主',
                           initial='root',
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'root',
                                                         }), )

    permission = forms.IntegerField(required=False, label='文件权限',
                           initial=755,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 755,
                                                         }), )
    content = forms.CharField(required=False, label='备注',
                           # initial='root',
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': '如：nginx配置修改',
                                                         }), )

class FileDownForm(forms.Form):
    # inventory = forms.ChoiceField(choices=(('1','产品线'),('2','组别'),('3','动态资产表'),('4','自定义')),
    #                               required=True,label='资产类型',
    #                                widget=forms.Select(attrs={'class': 'form-control'}))
    inventory = forms.ModelChoiceField(queryset=Ansible_Inventory.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    filepath = forms.CharField(required=True, label='目标路径',
                           error_messages={'required': u'请输入目标路径', 'invalid': u'格式错误'},
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': '/usr/local/src/',
                                                         }), )
    content = forms.CharField(required=False, label='备注',
                              # initial='root',
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '如：nginx配置修改',
                                                            }), )
