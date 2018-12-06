#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

from models import *


class AssetForm(forms.Form):
    asset_type_choice = (
        ('server', '物理机'),
        ('vmserver', '虚拟机'),
        ('docker', '容器'),
        ('netdevice', '网络设备'),
        ('storagedevice', '存储设备'),
        ('others', '其他'),
    )
    asset_status_choice = (
        ('1', '在线'),
        ('2', '下线'),
        ('3', '故障'),
        ('4', '备用'),
        ('5', '未知'),
    )
    asset_type = forms.ChoiceField(required=True, choices=asset_type_choice, label='资产类型', initial='vmserver',
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(required=True, label='资产名称',
                           error_messages={'required': u'请输入资产名称', 'invalid': u'名格式错误'},
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': '资产名称',
                                                         }), )
    sn = forms.CharField(required=True, label='资产SN',
                         error_messages={'required': u'请输入资产SN', 'invalid': u'SN格式错误'},
                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                       'placeholder': '资产SN',
                                                       }), )
    status = forms.ChoiceField(required=True, choices=asset_status_choice, label='资产状态', initial='1',
                               widget=forms.Select(attrs={'class': 'form-control'}))
    business_unit = forms.ModelChoiceField(required=False, error_messages={'required': u'选择业务线'},
                                           queryset=BusinessUnit.objects.all(),
                                           widget=forms.Select(attrs={'class': 'form-control'}))

    asset_model = forms.CharField(label='资产型号', required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': '资产型号', }), )
    manufacturer = forms.CharField(label='供应商', required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': '供应商', }), )
    site = forms.CharField(label='放置区域', required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': '放置区域', }), )
    manage_ip = forms.GenericIPAddressField(required=False, error_messages={'required': u'请输入管理ip',
                                                                            'invalid': u'ip地址错误'}, label='管理ip',
                                            widget=forms.TextInput(
                                                attrs={'class': 'form-control', 'placeholder': '管理IP', }), )
    manager = forms.CharField(label='管理人员', required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '管理人员', }), )

    # buy_time = forms.DateField(label='购买时间',required=False,
    #                            widget=forms.DateInput(attrs={'class': 'form-control', }), )
    # expire_date = forms.DateField(label='过保时间',
    #                                   widget=forms.DateInput(attrs={'class': 'form-control', }), )
    buy_time = forms.CharField(label='购买时间', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'yyyy-mm-dd', }), )
    expire_date = forms.CharField(label='过保时间', required=False,
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control', 'placeholder': 'yyyy-mm-dd', }), )

    hosted_on = forms.ModelChoiceField(required=False, error_messages={'required': u'选择业务线'},
                                       queryset=Server_asset.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    raid_type = forms.CharField(label='raid类型', required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'raid类型', }), )

    hostname = forms.CharField(label='主机名', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': '主机名', }), )
    username = forms.CharField(label='主机用户名', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': '主机用户名', }), )
    passwd = forms.CharField(required=False, label=u'主机密码', error_messages={'required': u'密码不能为空'},
                             widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    sudo_passwd = forms.CharField(required=False, label=u'主机sudo密码', error_messages={'required': u'密码不能为空'},
                                  widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    keyfile = forms.CharField(required=False, label='keyfile路径',
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '/root/.ssh/rsd/', }), )
    port = forms.IntegerField(required=False, label='主机ssh端口',
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '22', }), )
    line = forms.CharField(required=False, label='线路',
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': '出口线路', }), )
    cpu_model = forms.CharField(required=False, label='CPU型号',
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'cpu型号', }), )
    cpu_number = forms.CharField(required=False, label='CPU个数',
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'cpu个数', }), )
    cpu_core = forms.CharField(label='CPU核数',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'cpu核数', }), )
    disk_total = forms.CharField(required=False, label='磁盘容量',
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': '磁盘容量', }), )
    ram_total = forms.CharField(required=False, label='内存容量',
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': '内存容量', }), )
    swap = forms.CharField(required=False, label='swap',
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'swap', }), )

    os_type = forms.ChoiceField(required=False, label='操作系统类型',
                                choices=(('1', 'linux'), ('2', 'windows'), ('3', 'mac')), initial='1',
                                widget=forms.Select(attrs={'class': 'form-control',
                                                           'placeholder': '操作系统', }), )
    os_distribution = forms.CharField(required=False, label='发行版本',
                                      widget=forms.TextInput(attrs={'class': 'form-control',
                                                                    'placeholder': '发行版本', }), )
    os_release = forms.CharField(required=False, label='操作系统版本',
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': '操作系统版本', }), )
    created_by = forms.CharField(required=False, label='录入方式', disabled=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'value': 'manual', }), )


class BusinessForm(forms.ModelForm):
    class Meta:
        model = BusinessUnit
        # exclude = ('id',)
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'parent_unit': forms.TextInput(attrs={'class': 'form-control'}),
            'memo': forms.TextInput(attrs={'class': 'form-control'}),
            'manager': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service_Assets
        # exclude = ('id',)
        fields = '__all__'
        widgets = {
            'business': forms.TextInput(attrs={'class': 'form-control'}),
            'service_name': forms.TextInput(attrs={'class': 'form-control'}),
            'memo': forms.TextInput(attrs={'class': 'form-control'}),
            'manager': forms.TextInput(attrs={'class': 'form-control'}),
        }
# class NewAssetForm(forms.ModelForm):
#     class Meta:
#         model = NewAssetApprovalZone
#         fields = ['asset_type', 'sn', 'model', 'manufacturer', 'c_time', 'm_time']
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#             'password': forms.PasswordInput(attrs={'class': 'form-control'}),
#             'email': forms.TextInput(attrs={'class': ' form-control'}),
#             'role': forms.Select(attrs={'class': 'form-control'}),
#             'is_active': forms.Select(choices=((True, u'启用'), (False, u'禁用')), attrs={'class': 'form-control'}),
#         }
#
#     def __init__(self, *args, **kwargs):
#         super(NewAssetForm, self).__init__(*args, **kwargs)
#         self.fields['username'].label = u'账 号'
#         self.fields['username'].error_messages = {'required': u'请输入账号'}
#         self.fields['password'].label = u'密 码'
#         self.fields['password'].error_messages = {'required': u'请输入密码'}
#         self.fields['email'].label = u'邮 箱'
#         self.fields['email'].error_messages = {'required': u'请输入邮箱', 'invalid': u'请输入有效邮箱'}
#
#         self.fields['role'].label = u'角 色'
#         self.fields['is_active'].label = u'状 态'
