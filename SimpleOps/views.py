#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from accounts.permission import permission_verify
from cmdb import models
from deploy.models import Global_Config, Email_Config


# Create your views here.
@login_required()
@permission_verify()
def index(request):
    total = models.Assets.objects.count()
    upline = models.Assets.objects.filter(status='1').count()
    offline = models.Assets.objects.filter(status='2').count()
    unknown = models.Assets.objects.filter(status='5').count()
    breakdown = models.Assets.objects.filter(status='3').count()
    backup = models.Assets.objects.filter(status='4').count()
    total = float(total)  # python2 运算时需要浮点数时，必须设置其中一个数是浮点数，否则只能得到整数
    up_rate = round(upline / total * 100)
    o_rate = round(offline / total * 100)
    un_rate = round(unknown / total * 100)
    bd_rate = round(breakdown / total * 100)
    bu_rate = round(backup / total * 100)
    server_number = models.Server_asset.objects.count()
    networkdevice_number = models.Network_asset.objects.count()
    storagedevice_number = models.Disk_asset.objects.count()
    securitydevice_number = models.SecurityDevice.objects.count()
    software_number = models.Middleware.objects.count()
    return render(request, 'dashboard.html', locals())


def page_not_found(request):
    return render(request, 'pages-404.html', {}, status=404)


def page_not_permission(request):
    return render(request, 'pages-403.html', {}, status=403)


def internl_error(request):
    return render(request, 'pages-500.html', {}, status=500)


def bad_request(request):
    return render(request, 'pages-400.html', {}, status=400)


@login_required
@permission_verify()
def config(request):
    if request.method == "GET":
        try:
            config = Global_Config.objects.get(id=1)
        except:
            config = None
        try:
            email = Email_Config.objects.get(id=1)
        except:
            email = None
        return render(request, 'config.html', {"user": request.user, "config": config,
                                                      "email": email})
    elif request.method == "POST":
        if request.POST.get('op') == "log":
            try:
                count = Global_Config.objects.filter(id=1).count()
            except:
                count = 0
            if count > 0:
                Global_Config.objects.filter(id=1).update(
                    ansible_model=request.POST.get('ansible_model'),
                    ansible_playbook=request.POST.get('ansible_playbook'),
                    cron=request.POST.get('cron'),
                    project=request.POST.get('project'),
                    assets=request.POST.get('assets', 0),
                    server=request.POST.get('server', 0),
                    email=request.POST.get('email', 0),
                    webssh=request.POST.get('webssh', 0),
                    sql=request.POST.get('sql', 0),
                )
            else:
                config = Global_Config.objects.create(
                    ansible_model=request.POST.get('ansible_model'),
                    ansible_playbook=request.POST.get('ansible_playbook'),
                    cron=request.POST.get('cron'),
                    project=request.POST.get('project'),
                    assets=request.POST.get('assets'),
                    server=request.POST.get('server'),
                    email=request.POST.get('email'),
                    webssh=request.POST.get('webssh', 0),
                    sql=request.POST.get('sql'),
                )
            return JsonResponse({'msg': '配置修改成功', "code": 200, 'data': []})
        elif request.POST.get('op') == "email":
            try:
                count = Email_Config.objects.filter(id=1).count()
            except:
                count = 0
            if count > 0:
                Email_Config.objects.filter(id=1).update(
                    site=request.POST.get('site'),
                    host=request.POST.get('host', None),
                    port=request.POST.get('port', None),
                    user=request.POST.get('user', None),
                    passwd=request.POST.get('passwd', None),
                    subject=request.POST.get('subject', None),
                    cc_user=request.POST.get('cc_user', None),
                )
            else:
                Email_Config.objects.create(
                    site=request.POST.get('site'),
                    host=request.POST.get('host', None),
                    port=request.POST.get('port', None),
                    user=request.POST.get('user', None),
                    passwd=request.POST.get('passwd', None),
                    subject=request.POST.get('subject', None),
                    cc_user=request.POST.get('cc_user', None),
                )
            return JsonResponse({'msg': '配置修改成功', "code": 200, 'data': []})
