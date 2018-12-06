# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django_celery_beat.models import IntervalSchedule,CrontabSchedule,PeriodicTask,SolarSchedule
from django_celery_results.models import TaskResult
from . import forms
# Create your views here.
@login_required
def index(request):
    data_list = PeriodicTask.objects.all()
    return render(request,"setup_jobs/jobs.html",{"data_list":data_list})


@login_required
def task_result(request):
    data_list = TaskResult.objects.all().order_by("-id")
    return render(request,"setup_jobs/task_result.html",{"data_list":data_list})


@login_required
def task_result_del(request,result_id):
    obj = TaskResult.objects.get(id=result_id)
    obj.delete()
    message = "删除成功"
    data_list = TaskResult.objects.all()
    return render(request, "setup_jobs/task_result.html", locals())

@login_required
def job_add(request):

    if request.method == "POST":
        form = forms.PeriodicForm(request.POST)
        if form.is_valid():
            form.save()
            message = "任务新增成功"
        else:
            message = "任务新增失败"
    else:
        form = forms.PeriodicForm()
    return render(request,"setup_jobs/job_add.html",locals())

@login_required
def job_edit(request,job_id):
    jobobj = PeriodicTask.objects.get(id=job_id)
    if request.method == "POST":
        form = forms.PeriodicForm(request.POST,instance=jobobj) #必须同时传入post数据和实例数据，否则不能修改
        if form.is_valid():
            form.save()
        message = "任务修改成功"
    else:
        form = forms.PeriodicForm(instance=jobobj)
    return render(request,"setup_jobs/job_edit.html",locals())

@login_required
def job_del(request,job_id):
    jobobj = PeriodicTask.objects.get(id=job_id)
    jobobj.delete()
    message = "删除成功"
    data_list = PeriodicTask.objects.all()
    return render(request, "setup_jobs/jobs.html", locals())


@login_required
def cron_add(request):
    status = ""
    if request.method == "POST":
        form = forms.CrontabForm(request.POST)
        if form.is_valid():
            form.save()
            message = "任务新增成功"
            status = 1
        else:
            status = 2
    else:
        form = forms.CrontabForm()
    return render(request,"setup_jobs/cron_add.html",locals())

@login_required
def cron_edit(request,cron_id):
    status = ""
    cronobj = CrontabSchedule.objects.get(id=cron_id)
    if request.method == "POST":
        form = forms.CrontabForm(request.POST,instance=cronobj) #必须同时传入post数据和实例数据，否则不能修改
        if form.is_valid():
            form.save()
            message = "任务修改成功"
            status = 1
        else:
            status = 2
    else:
        form = forms.CrontabForm(instance=cronobj)
    return render(request,"setup_jobs/cron_edit.html",locals())


@login_required
def interval_add(request):
    if request.method == "POST":
        form = forms.IntervalForm(request.POST)
        if form.is_valid():
            form.save()
            message = "任务新增成功"
            status = 1
        else:
            status = 2
    else:
        form = forms.IntervalForm()
    return render(request,"setup_jobs/interval_add.html",locals())

@login_required
def interval_edit(request,interval_id):
    intervalobj = IntervalSchedule.objects.get(id=interval_id)
    if request.method == "POST":
        form = forms.IntervalForm(request.POST,instance=intervalobj) #必须同时传入post数据和实例数据，否则不能修改
        if form.is_valid():
            form.save()
            message = "任务修改成功"
            status = 1
        else:
            status = 2
    else:
        form = forms.IntervalForm(instance=intervalobj)
    return render(request,"setup_jobs/interval_edit.html",locals())



@login_required
def solar_add(request):
    if request.method == "POST":
        form = forms.SolarForm(request.POST)
        if form.is_valid():
            form.save()
            message = "任务新增成功"
            status = 1
        else:
            status = 2
    else:
        form = forms.SolarForm()
    return render(request,"setup_jobs/solar_add.html",locals())

@login_required
def solar_edit(request,solar_id):
    solarobj = SolarSchedule.objects.get(id=solar_id)
    if request.method == "POST":
        form = forms.SolarForm(request.POST,instance=solarobj) #必须同时传入post数据和实例数据，否则不能修改
        if form.is_valid():
            form.save()
            message = "任务修改成功"
            status = 1
        else:
            status = 2
    else:
        form = forms.SolarForm(instance=solarobj)
    return render(request,"setup_jobs/solar_edit.html",locals())