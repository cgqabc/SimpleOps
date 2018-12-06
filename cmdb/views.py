# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
import sys

import xlrd
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from accounts.permission import permission_verify
from common import token_check
from django.http import JsonResponse
from . import forms
from . import models, asset_handler
import logging
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger('django.cmdb')

# Create your views here.
@login_required(login_url='/login/')
@permission_verify()
def assets_info(request):
    user_name = request.user
    if request.method == "POST":
        message = "批量导入成功"
    asset_data = models.Assets.objects.all()
    return render(request, 'cmdb/assets.html', locals())


@login_required(login_url='/login/')
@permission_verify()
def detail(request, asset_id):
    user_name = request.user
    asset = get_object_or_404(models.Assets, id=asset_id)
    return render(request, 'cmdb/detail.html', locals())


@login_required(login_url='/login')
@permission_verify()
# @csrf_exempt
def assets_server_query(request):
    if request.method == "POST":
        if request.POST.get('query') in ['service','project','group']:
            dataList = []
            if request.POST.get('query') == 'service':
                for ser in models.Assets.objects.filter(service=request.POST.get('id')):#,assets_type__in=['server','vmser','switch','route']):
                    try:
                        project = ser.business_unit.name
                    except Exception,ex:
                        project = '未知'
                        logger.warn(msg="查询主机产品线信息失败: {ex}".format(ex=str(ex)))
                    try:
                        service = models.Service_Assets.objects.get(id=ser.service).service_name
                    except Exception,ex:
                        service = '未知'
                        logger.warn(msg="查询主机业务类型失败: {ex}".format(ex=str(ex)))
                    if ser.asset_type in ['server','vmser']:dataList.append({"id":ser.server_asset.id,"ip":ser.server_asset.ip,"project":project,"service":service})
                    elif ser.asset_type in ['switch','route']:dataList.append({"id":ser.network_asset.id,"ip":ser.network_asset.ip,"project":project,"service":service})
            elif request.POST.get('query') == 'group':
                for ser in models.Assets.objects.filter(group=request.POST.get('id')):#assets_type__in=['server','vmser','switch','route']):
                    try:
                        project = ser.business_unit.name
                    except Exception,ex:
                        project = '未知'
                        logger.warn(msg="查询主机产品线信息失败: {ex}".format(ex=str(ex)))
                    try:
                        service = models.Service_Assets.objects.get(id=ser.service).service_name
                    except Exception,ex:
                        service = '未知'
                        logger.warn(msg="查询主机业务类型失败: {ex}".format(ex=str(ex)))
                    if ser.asset_type in ['server','vmser']:dataList.append({"id":ser.server_asset.id,"ip":ser.server_asset.ip,"project":project,"service":service})
                    elif ser.asset_type in ['switch','route']:dataList.append({"id":ser.network_asset.id,"ip":ser.network_asset.ip,"project":project,"service":service})
            return JsonResponse({'msg':"主机查询成功","code":200,'data':dataList})
        else:JsonResponse({'msg':"不支持的操作","code":500,'data':[]})
    else:
        return JsonResponse({'msg':"操作失败","code":500,'data':"不支持的操作"})


@login_required(login_url='/login/')
@permission_verify()
def asset_add(request):
    user_name = request.user
    if request.method == "POST":
        form = forms.AssetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            defaults = {
                'data': json.dumps(data),
                'asset_type': data.get('asset_type'),
                'manufacturer': data.get('provider'),
                'model': data.get('asset_model'),
                'ram_size': data.get('ram_size'),
                'cpu_model': data.get('cpu_model'),
                'cpu_number': data.get('cpu_number'),
                'cpu_core': data.get('cpu_core'),
                'os_distribution': data.get('os_distribution'),
                'os_release': data.get('os_release'),
                'os_type': data.get('os_type'),
            }
            models.NewAssetApprovalZone.objects.update_or_create(sn=data['sn'], defaults=defaults)
            message = "资产新增成功"
    else:
        form = forms.AssetForm()
    return render(request, 'cmdb/asset_add.html', locals())


@login_required(login_url='/login/')
@permission_verify()
def asset_edit(request, asset_id):
    user_name = request.user
    if request.method == "POST":
        form = forms.AssetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            asset_obj = models.Assets.objects.filter(sn=str(data['sn']))
            update_asset = asset_handler.UpdateAsset(request, asset_obj[0], data)
            result = update_asset.asset_update()
            if not result:
                message = "资产修改成功"
            else:
                message = "资产修改失败：%s" % str(result).decode('unicode_escape') #todo 输出有问题
    else:
        asset = get_object_or_404(models.Assets, id=asset_id)
        data = asset.__dict__
        if getattr(asset, 'server_asset', None):
            s = asset.server_asset.__dict__
            # 反向查询时，外键和多对多采用asset.server_asset_set的方式查询，一对一则直接查询
            data['hosted_on'] = s.get('hosted_on', None)
            data['raid_type'] = s.get('raid_type', None)
            data['username'] = s.get('username', None)
            data['hostname'] = s.get('hostname', None)
            data['keyfile'] = s.get('keyfile', None)
            data['port'] = s.get('port', None)
            data['disk_total'] = s.get('disk_total', None)
            data['ram_total'] = s.get('ram_total', None)
            data['swap'] = s.get('swap', None)
            data['os_type'] = s.get('os_type', None)
            data['os_distribution'] = s.get('os_distribution', None)
            data['os_release'] = s.get('os_release', None)

        if getattr(asset, 'cpu', None):
            s = asset.cpu.__dict__
            data['cpu_model'] = s.get('cpu_model', None)
            data['cpu_number'] = s.get('cpu_number', None)
            data['cpu_core'] = s.get('cpu_core', None)
        form = forms.AssetForm(data)
    return render(request, 'cmdb/asset_edit.html', locals())


@login_required(login_url='/login/')
@permission_verify()
def asset_del(request, asset_id):
    user_name = request.user
    asset = get_object_or_404(models.Assets, id=asset_id)
    asset.delete()
    asset_data = models.Assets.objects.all()
    return render(request, 'cmdb/assets.html', locals())


@login_required(login_url='/login/')
@permission_verify()
def new_asset_permission(request):
    user_name = request.user
    asset_data = models.NewAssetApprovalZone.objects.all()
    return render(request, 'cmdb/new_asset.html', locals())


@login_required(login_url='/login/')
@permission_verify()
def new_asset_allow(request, asset_id):
    user_name = request.user
    try:
        obj = asset_handler.ApproveAsset(request, asset_id)
        ret = obj.asset_upline()
        message = "新增成功！"
    except Exception as e:
        message = "新增失败：%s" % e
    asset_data = models.NewAssetApprovalZone.objects.all()
    return render(request, 'cmdb/new_asset.html', locals())


@login_required(login_url='/login/')
@permission_verify()
def new_asset_del(request, asset_id):
    user_name = request.user
    asset = models.NewAssetApprovalZone.objects.get(id=asset_id)
    asset.delete()
    message = "删除成功！"
    asset_data = models.NewAssetApprovalZone.objects.all()
    return render(request, 'cmdb/new_asset.html', locals())


@login_required(login_url='/login/')
@permission_verify()
def asset_batch_import(request):
    if request.method == "POST":
        fileobj = request.FILES.get("batch_import")
        filename = os.path.join(os.getcwd(), 'upload', fileobj.name)
        # if os.path.isdir(os.path.dirname(filename)) is not True:
        if not os.path.exists(os.path.join(os.getcwd(), 'upload')):
            # print("dir not exists,make it")
            os.makedirs(os.path.join(os.getcwd(), 'upload'))
        try:
            with open(filename, 'wb') as f:
                for chunk in fileobj.chunks():
                    f.write(chunk)
        except Exception as e:
            print e
        data_list = []
        file = xlrd.open_workbook(filename)
        server = file.sheet_by_name("server")
        net = file.sheet_by_name("net")
        for i in range(1, server.nrows):
            data_list.append(server.row_values(i))
        # for i in range(1, net.nrows):
        #     data_list.append(net.row_values(i))
        try:
            for data in data_list:
                    defaults = {
                        'data': json.dumps({
                            'status': data[17],
                            'site': data[18],
                            'manage_ip': data[5],
                            'manager': data[6],
                            'buy_time': data[3],
                            'expire_date': data[4],
                            'hosted_on': data[23],
                            'raid_type': data[30],
                            'hostname': data[28],
                            'username': data[26],
                            'passwd': data[27],
                            'port': data[29],
                            'line': data[31],
                            'disk_total': data[11],
                        }),
                        'asset_type': data[0],
                        'manufacturer': data[9],
                        'model': data[8],
                        'ram_size': data[10],
                        'cpu_model': data[15],
                        'cpu_number': int(data[16]),
                        'cpu_core': int(data[17]),
                        'os_distribution': data[14],
                        'os_release': data[13],
                        'os_type': data[12],
                    }
                    # print json.dumps(defaults,indent=4)
                    models.NewAssetApprovalZone.objects.update_or_create(sn=data[1], defaults=defaults)
        except Exception as e:
            print e
            return HttpResponse("资产新增失败",status=500)
        else:
            return HttpResponse("资产批量新增成功")


@login_required(login_url='/login/')
@permission_verify()
def project(request):
    user_name = request.user
    asset_data = models.Assets.objects.all()
    return render(request, 'cmdb/assets.html', locals())


@login_required(login_url='/login/')
@permission_verify()
def business_unit(request):
    user_name = request.user
    bus_data = models.BusinessUnit.objects.all()
    return render(request, 'cmdb/business_info.html', locals())

@login_required(login_url='/login/')
@permission_verify()
def business_add(request):
    user_name = request.user
    if request.method == "POST":
        bus_data = forms.BusinessForm(request.POST)
        if bus_data.is_valid():
            bus_data.save()
            message = "操作成功"
    else:
        bus_data = forms.BusinessForm()
    return render(request, 'cmdb/business_add.html', locals())

@login_required(login_url='/login/')
@permission_verify()
def business_edit(request,bus_id):
    user_name = request.user
    busobj = models.BusinessUnit.objects.get(id=bus_id)
    if request.method == "POST":
        bus_data = forms.BusinessForm(request.POST,instance=busobj)
        if bus_data.is_valid():
            bus_data.save()
            message = "操作成功"
    else:
        bus_data = forms.BusinessForm(instance=busobj)
    return render(request, 'cmdb/business_edit.html', locals())

@login_required(login_url='/login/')
@permission_verify()
def business_del(request,bus_id):
    busobj = models.BusinessUnit.objects.get(id=bus_id)
    busobj.delete()
    return HttpResponse("删除成功")



@login_required(login_url='/login/')
@permission_verify()
def project_list(request):
    user_name = request.user
    bus_data = models.Service_Assets.objects.all()
    return render(request, 'cmdb/project_list.html', locals())

@login_required(login_url='/login/')
@permission_verify()
def project_add(request):
    user_name = request.user
    if request.method == "POST":
        bus_data = forms.ServiceForm(request.POST)
        if bus_data.is_valid():
            bus_data.save()
            message = "操作成功"
    else:
        bus_data = forms.ServiceForm()
    return render(request, 'cmdb/project_add.html', locals())

@login_required(login_url='/login/')
@permission_verify()
def project_edit(request,bus_id):
    user_name = request.user
    busobj = models.Service_Assets.objects.get(id=bus_id)
    if request.method == "POST":
        bus_data = forms.ServiceForm(request.POST,instance=busobj)
        if bus_data.is_valid():
            bus_data.save()
            message = "操作成功"
    else:
        bus_data = forms.ServiceForm(instance=busobj)
    return render(request, 'cmdb/project_edit.html', locals())

@login_required(login_url='/login/')
@permission_verify()
def project_del(request,bus_id):
    busobj = models.Service_Assets.objects.get(id=bus_id)
    busobj.delete()
    return HttpResponse("删除成功")



mytoken = "uDRpMS8MoyCr6SZ5"


@csrf_exempt
@token_check(mytoken)
def report(request):
    """
    通过csrf_exempt装饰器，跳过Django的csrf安全机制，让post的数据能被接收，但这又会带来新的安全问题。
    可以在客户端，使用自定义的认证token，进行身份验证。
    """
    if request.method == "POST":
        asset_data = request.POST.get('asset_data')
        data = json.loads(asset_data)
        # 各种数据检查，请自行添加和完善！
        if not data:
            return HttpResponse("没有数据！")
        if not issubclass(dict, type(data)):
            return HttpResponse("数据必须为字典格式！")
        # 是否携带了关键的sn号
        sn = data.get('sn', None)
        if sn:
            # 进入审批流程
            # 首先判断是否在上线资产中存在该sn
            asset_obj = models.Assets.objects.filter(sn=sn)
            if asset_obj:
                # 进入已上线资产的数据更新流程
                update_asset = asset_handler.UpdateAsset(request, asset_obj[0], data)
                info = update_asset.asset_update()
                if not info:
                    return HttpResponse("资产数据已经更新！")
                else:
                    return HttpResponse("资产数据失败：%s" % info)
            else:  # 如果已上线资产中没有，那么说明是未批准资产，进入新资产待审批区，更新或者创建资产。
                obj = asset_handler.New_asset(request, data)
                response = obj.add_to_new_assets_zone()
                return HttpResponse(response)
        else:
            return HttpResponse("没有资产sn序列号，请检查数据！")
    else:
        return HttpResponse("error,please use post")
