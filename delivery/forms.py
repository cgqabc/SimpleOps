#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

from .models import *





class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project_Config
        exclude = ('id','project_uuid')
        # fields = '__all__'
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'project_env': forms.Select(choices=(('sit', u'测试'), ('uat', u'预生产'),
                                                 ('prod', u'生产')),
                                        attrs={'class': 'form-control'}),
            'project_name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'project_service': forms.TextInput(attrs={'class': 'form-control'}),
            'project_service': forms.Select(attrs={'class': 'form-control'}),
            'project_type': forms.TextInput(attrs={'class': 'form-control'}),
            'project_local_command': forms.TextInput(attrs={'class': 'form-control'}),
            'project_repo_dir': forms.TextInput(attrs={'class': 'form-control'}),
            'project_dir': forms.TextInput(attrs={'class': 'form-control'}),
            'project_exclude': forms.TextInput(attrs={'class': 'form-control'}),
            'project_address': forms.TextInput(attrs={'class': 'form-control'}),
            'project_repo_user': forms.TextInput(attrs={'class': 'form-control'}),
            'project_repo_passwd': forms.TextInput(attrs={'class': 'form-control'}),
            'project_repertory': forms.Select(attrs={'class': 'form-control'}),
            'project_status': forms.Select(choices=((0, u'未激活'), (1, u'激活'),),
                                           attrs={'class': 'form-control'}),
            'project_remote_command': forms.TextInput(attrs={'class': 'form-control'}),
            'project_user': forms.TextInput(attrs={'class': 'form-control'}),
            'project_model': forms.Select(attrs={'class': 'form-control'}),
            'project_audit_group': forms.TextInput(attrs={'class': 'form-control','placeholder': '数值，如1'}),


        }


