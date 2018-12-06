#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
import json,os
from django_celery_beat.models import IntervalSchedule,CrontabSchedule,PeriodicTask,SolarSchedule
from django_celery_results.models import TaskResult
from celery import  current_app
from celery.utils import cached_property
from django.forms.widgets import Select
from kombu.utils.json import loads
# os.environ.setdefault("DJANGO_SETTINGS_MODULE","SimpleOps.settings")

class TaskSelectWidget(Select):
    """Widget that lets you choose between task names."""

    celery_app = current_app
    _choices = None

    def tasks_as_choices(self):
        _ = self._modules  # noqa   #noga表示不检查这句的代码质量
        tasks = list(sorted(name for name in self.celery_app.tasks
                            if not name.startswith('celery.')))
        return (('', ''), ) + tuple(zip(tasks, tasks))

    @property
    def choices(self):
        if self._choices is None:
            self._choices = self.tasks_as_choices()
        return self._choices

    @choices.setter
    def choices(self, _):
        # ChoiceField.__init__ sets ``self.choices = choices``
        # which would override ours.
        pass

    @cached_property
    def _modules(self):
        self.celery_app.loader.import_default_modules()


class TaskChoiceField(forms.ChoiceField):
    """Field that lets you choose between task names."""

    widget = TaskSelectWidget

    def valid_value(self, value):
        return True


class PeriodicForm(forms.ModelForm):
#     current_app.loader.import_default_modules() #加载所有的app内的task，，不生效，单独运行报错
#     tasks = list(sorted(name for name in current_app.tasks
#                         if not name.startswith('celery.'))) #排除内部任务
#     choices = (('', ''), ) + tuple(zip(tasks, tasks)) #添加一个空的二元组，使默认为空
#     regtask = forms.CharField(
#         label=('Task (registered)'),
#         required=False,
#         widget=forms.Select(choices=choices,
#             attrs={'class': 'form-control', 'style': 'width:450px;'}),
#     )

    regtask = TaskChoiceField(
        label=('Task (registered)'),
        required=False,
    )

    task = forms.CharField(
        label=('Task (custom)'),
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
    )

    # kwargs = forms.CharField(
    #     label=('任务指令'),
    #     required=False,
    #     max_length=200,
    #     initial='',
    #     widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;',
    #                                   'placeholder': u'{"host":"your_hostname","name":"scritps_name or command"}'})
    # )

    class Meta:
        model = PeriodicTask
        exclude = ()
        # fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            # 'task': forms.Select(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'args': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'kwargs': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            # 'interval': forms.Select(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            # 'crontab': forms.Select(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'enabled': forms.Select(choices=((True, u'启用'), (False, u'禁用')),
                                    attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'queue': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'exchange': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'routing_key': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'expires': forms.DateTimeInput(attrs={'class': 'form-control', 'style': 'width:450px;',
                                                  'placeholder': u'2017-06-23 10:11:11'}),
            'last_run_at': forms.DateTimeInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
        }
    def clean(self):
        data = super(PeriodicForm, self).clean()
        regtask = data.get('regtask')
        if regtask:
            data['task'] = regtask
        if not data['task']:
            exc = forms.ValidationError(('Need name of task'))
            self._errors['task'] = self.error_class(exc.messages)
            raise exc
        return data

    def _clean_json(self, field):
        value = self.cleaned_data[field]
        try:
            loads(value)
        except ValueError as exc:
            raise forms.ValidationError(
                ('Unable to parse JSON: %s') % exc,
            )
        return value

    def clean_args(self):
        return self._clean_json('args')

    def clean_kwargs(self):
        return self._clean_json('kwargs')

class IntervalForm(forms.ModelForm):

    class Meta:
        model = IntervalSchedule
        exclude = ("id",)


class CrontabForm(forms.ModelForm):

    class Meta:
        model = CrontabSchedule
        exclude = ("id",)

class SolarForm(forms.ModelForm):

    class Meta:
        model = SolarSchedule
        exclude = ("id",)

class TaskResultForm(forms.ModelForm):

    class Meta:
        model = TaskResult
        exclude = ("id",)
