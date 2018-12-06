# -*- coding: utf-8 -*-
import os,json
import uuid

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse,StreamingHttpResponse,FileResponse
from django.shortcuts import render_to_response, render
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from accounts.permission import permission_verify
from deploy.ansible_api_v2 import ANSRunner
from deploy.log_ansible import AnsibleRecord
from deploy.redis_ops import Redis_pool
from deploy.views import get_json_inentory
from .forms import *
from .models import LogFileOps


class finder(LoginRequiredMixin, View):
    @method_decorator(permission_verify())
    def get(self, request):
        temp_name = "mfile/mfile-header.html"
        return render_to_response('mfile/finder.html', locals())


@login_required()
@permission_verify()
def file_up(request):
    if request.method == "GET":
        form = FileUpForm()
        uuidkey = uuid.uuid4()
        return render(request, "mfile/file_up.html", locals())
    elif request.method == "POST":
        scripts_uuid = request.POST.get('uuidkey')
        form = FileUpForm(request.POST)

        if form.is_valid():
            descpath = form.cleaned_data['filepath']
            permission = form.cleaned_data['permission']
            owner = form.cleaned_data['owner']
            inventory = form.cleaned_data['inventory']
            content = form.cleaned_data['content']
            # print model,args,debug,inventory
            resource, sList = get_json_inentory(inventory.id, pw="get")

            fileobj = request.FILES.get("file_upload", None)
            # fileName = None
            filePath = None
            if fileobj:
                # fileName = os.path.join('/upload/myfile/upload', fileobj.name)
                filePath = os.path.join(os.getcwd(), 'upload/myfile/upload',fileobj.name)
                # if os.path.isdir(os.path.dirname(filename)) is not True:
                if not os.path.exists(os.path.join(os.getcwd(), 'upload/myfile/upload')):
                    # print("dir not exists,make it")
                    os.makedirs(os.path.join(os.getcwd(), 'upload/myfile/upload'))
                try:
                    with open(filePath, 'wb') as f:
                        for chunk in fileobj.chunks():
                            f.write(chunk)
                except Exception as e:
                    print e

                scripts_args = "src={} dest={} owner={} mode={} backup=yes".format(filePath,
                                                                                  descpath,
                                                                                   owner,permission )
                redisKey = scripts_uuid
                # logId = AnsibleRecord.Model.insert(user=str(request.user), ans_model='copy',
                #                                    ans_server=','.join(sList), ans_args=filePath)
                Redis_pool.delete(redisKey)
                Redis_pool.lpush(redisKey,
                                 "[Start] Ansible Model: {model}  Script:{filePath} {args}".format(
                                     model='copy', filePath=filePath, args=scripts_args))

                ANS = ANSRunner(resource, redisKey)

                ANS.run_model(host_list=sList, module_name='copy',
                              module_args=scripts_args)
                Redis_pool.lpush(redisKey, "[Done] Ansible Done.")
                try:
                    LogFileOps.objects.create(opstype="up",filepath=descpath,server=str(sList),
                                          content=content,
                                          user=str(request.user.username),srcfile=fileobj.name)
                except Exception as e:
                    print(e)
                return JsonResponse({'msg': "操作成功", "code": 200, 'data': []})

            else:
                # print "操作失败，未选择主机或者该分组没有成员"
                return JsonResponse({'msg': "操作失败，未选择主机或者该分组没有成员",
                                     "code": 500, 'data': []})
@login_required()
@permission_verify()
def file_find(request):
    if request.method == "POST":
        form = FileDownForm(request.POST)

        if form.is_valid():
            descpath = form.cleaned_data['filepath']
            inventory = form.cleaned_data['inventory']
            dataList = []
            resource, sList = get_json_inentory(inventory.id, pw="get")
            scripts_args = "path={}".format(descpath)
            ANS = ANSRunner(resource)
            ANS.run_model(host_list=sList, module_name='find',
                          module_args=scripts_args)
            filesData = json.loads(ANS.get_model_result())
            for k, v in filesData.get('success').items():
                for ds in v.get('files'):
                    data = {}
                    # data["id"] = order.id
                    data['host'] = k
                    data['path'] = ds.get('path')
                    data['size'] = round(float(ds.get('size'))/1024,2)
                    data['islnk'] = ds.get('islnk')
                    dataList.append(data)
            return JsonResponse({'msg': "操作成功", "code": 200, 'data': dataList})
        else:
            return JsonResponse({'msg': "操作失败", "code": 500, 'data': []})


@login_required()
@permission_verify()
def file_down(request):
    if request.method == "GET":
        form = FileDownForm()
        uuidkey = uuid.uuid4()
        return render(request, "mfile/file_down.html", locals())


    elif request.method == "POST":

        descpath = request.POST.get('path')
        inventory = request.POST.get('inventory')
        content = request.POST.get('content')
        # print model,args,debug,inventory
        resource, sList = get_json_inentory(inventory, pw="get")

        filePath = os.path.join(os.getcwd(),'upload/myfile/download')
        if not os.path.exists(filePath):
            # print("dir not exists,make it")
            os.makedirs(filePath)

        scripts_args = "src={} dest={} fail_on_missing=yes".format(descpath,filePath,)
        ANS = ANSRunner(resource)
        ANS.run_model(host_list=sList, module_name='fetch',
                      module_args=scripts_args)
        # 日志记录
        try:
            LogFileOps.objects.create(opstype="down",filepath='/upload/myfile/download',
                                      server=str(sList),content=content,
                                      user=str(request.user.username),srcfile=descpath)
        except Exception as e:
            print(e)
        # 文件读取迭代
        def file_iterator(filepath,chunk_size=512):
            with open(filepath,'rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        result = json.loads(ANS.get_model_result())
        filePath = result.get('success').get(request.POST.get('dest_server')).get('dest')
        if filePath:
            response = StreamingHttpResponse(file_iterator(filePath))
            response = FileResponse(response)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment; filename="{file_name}'.format(
                file_name=os.path.basename(filePath))
            return response

        # return JsonResponse({'msg': "操作成功", "code": 200, 'data': []})

        else:
            # print "操作失败，未选择主机或者该分组没有成员"
            return JsonResponse({'msg': "操作失败，未选择主机或者该分组没有成员",
                                 "code": 500, 'data': []})

@login_required()
@permission_verify()
def file_log(request):
    if request.method == "GET":
        data_list = LogFileOps.objects.all()
        uuidkey = uuid.uuid4()
        return render(request, "mfile/file_log.html", locals())
