# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import uuid

import os
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

from accounts.permission import permission_verify
from .ansible_api_v2 import ANSRunner
from .forms import InventoryForm, GroupForm, MoudelForm, ScriptsForm, PlaybookForm
from .log_ansible import AnsibleRecord
from .models import (Ansible_Inventory, Ansible_Group, Ansible_Server, Assets,
                     Ansible_Script, Ansible_Playbook, Log_Ansible_Playbook, Log_Ansible_Model, )
from .redis_ops import Redis_pool


# Create your views here.
@login_required
@permission_verify()
def inventory(request):
    if request.method == "GET":
        data_list = Ansible_Inventory.objects.all()
        # detail = {}
        for d in data_list:
            i, _ = get_json_inentory(d.id)
            d.detail = json.dumps(i, indent=4)

        return render(request, "deploy/inventory.html", {"data_list": data_list})


def get_json_inentory(inventory_id, pw=None):
    try:
        i = Ansible_Inventory.objects.get(id=inventory_id)
        data = {}
        all_host = []
        for x in i.inventory_group.all():
            data[x.group] = {}
            hosts = []
            if pw:
                for y in x.inventory_server.all():
                    y = Assets.objects.get(id=y.server)
                    hosts.append({"ip": y.manage_ip,
                                  "username": y.server_asset.username,
                                  "password": y.server_asset.passwd,
                                  "sudo_passwd": y.server_asset.sudo_passwd, })
                    all_host.append(y.manage_ip)
            else:
                for y in x.inventory_server.all():
                    y = Assets.objects.get(id=y.server)
                    hosts.append({"ip": y.manage_ip, })
                    all_host.append(y.manage_ip)
            data[x.group]["hosts"] = hosts
            if x.ext_vars:
                data[x.group]["vars"] = json.loads(x.ext_vars)
        # print data,all_host
        return data, all_host

    except Exception as e:
        print e
        return e


@login_required
@permission_verify()
def inventory_add(request):
    if request.method == "GET":
        inventory_form = InventoryForm()
        group_form = GroupForm()
        return render(request, "deploy/inventory_add.html", locals())
    else:
        inventory_form = InventoryForm(request.POST)
        group_form = GroupForm(request.POST)
        if inventory_form.is_valid():
            name = inventory_form.cleaned_data["name"]
            desc = inventory_form.cleaned_data["desc"]
            create_user = request.user
            Ansible_Inventory.objects.update_or_create(name=name, desc=desc, create_user=create_user)
            message = "新增成功"
            return render(request, "deploy/inventory_add.html", locals())
        elif group_form.is_valid():
            inventory = group_form.cleaned_data["inventory"]
            group = group_form.cleaned_data["group"]
            ext_vars = group_form.cleaned_data["ext_vars"]
            # g = Ansible_Group(inventory=inventory,group=group,ext_vars=ext_vars)
            # g.save()
            # get_or_create 以及 update_or_create方法都要使用defaults的方式
            default = {"inventory": inventory, "group": group, "ext_vars": ext_vars}
            g, _ = Ansible_Group.objects.update_or_create(defaults=default, group=group)
            server = group_form.cleaned_data["server"]
            for i in server:
                default = {"group": g, "server": i.id}
                Ansible_Server.objects.update_or_create(defaults=default, group=g, server=i.id)
            message = "新增成功"
            return render(request, "deploy/inventory_add.html", locals())


@login_required
@permission_verify()
def inventory_edit(request, in_id):
    inventory_data = Ansible_Inventory.objects.get(id=in_id)
    group_data = inventory_data.inventory_group.all()[0]

    if request.method == "GET":
        inventory_form = InventoryForm(model_to_dict(inventory_data))
        group_form = GroupForm(model_to_dict(group_data))
        return render(request, "deploy/inventory_add.html", locals())
    else:
        inventory_form = InventoryForm(request.POST, model_to_dict(inventory_data))
        group_form = GroupForm(request.POST, model_to_dict(group_data))
        if inventory_form.is_valid():
            name = inventory_form.cleaned_data["name"]
            desc = inventory_form.cleaned_data["desc"]
            create_user = request.user
            Ansible_Inventory.objects.update_or_create(name=name, desc=desc, create_user=create_user)
            message = "修改成功"
            return render(request, "deploy/inventory_add.html", locals())
        elif group_form.is_valid():
            inventory = group_form.cleaned_data["inventory"]
            group = group_form.cleaned_data["group"]
            ext_vars = group_form.cleaned_data["ext_vars"]
            # g = Ansible_Group(inventory=inventory,group=group,ext_vars=ext_vars)
            # g.save()
            # get_or_create 以及 update_or_create方法都要使用defaults的方式
            default = {"inventory": inventory, "group": group, "ext_vars": ext_vars}
            g, _ = Ansible_Group.objects.update_or_create(defaults=default, group=group)
            server = group_form.cleaned_data["server"]
            for i in server:
                default = {"group": g, "server": i.id}
                Ansible_Server.objects.update_or_create(defaults=default, group=g, server=i.id)
            message = "新增成功"
            return render(request, "deploy/inventory_add.html", locals())


@login_required
@permission_verify()
def inventory_del(request, in_id):
    if request.method == "GET":
        Ansible_Inventory.objects.get(id=in_id).delete()
        data_list = Ansible_Inventory.objects.all()

        for d in data_list:
            i, _ = get_json_inentory(d.id)
            d.detail = json.dumps(i, indent=4)
        return render(request, "deploy/inventory.html", {"data_list": data_list})


@login_required()
def get_ansibel_result(request):
    if request.method == "POST":
        redisKey = request.POST.get('uuidkey')
        msg = Redis_pool.rpop(redisKey)
        if msg:
            return JsonResponse({'msg': msg, "code": 200, 'data': []})
        else:
            return JsonResponse({'msg': None, "code": 200, 'data': []})


@login_required
@permission_verify()
def moudel_run(request):
    if request.method == "POST":
        redisKey = request.POST.get('uuidkey')
        form = MoudelForm(request.POST)

        if form.is_valid():
            model = form.cleaned_data['moudel']
            args = form.cleaned_data['moudel_args']
            debug = form.cleaned_data['_debug']
            inventory = form.cleaned_data['inventory']
            # print model,args,debug,inventory
            resource, sList = get_json_inentory(inventory.id, pw="get")

            if len(sList) > 0:
                # 使用日志全局配置设置
                logId = AnsibleRecord.Model.insert(user=str(request.user), ans_model=model,
                                                   ans_server=','.join(sList), ans_args=args)
                # logId = Log_Ansible_Model.objects.create(
                #     ans_user=str(request.user),
                #     ans_server=','.join(sList),
                #     ans_args=args,
                #     ans_model=model,
                # )
                Redis_pool.delete(redisKey)
                Redis_pool.lpush(redisKey,
                                 "[Start] Ansible Model: {0}  ARGS:{1}".format(model, args))

                if debug == 'on':
                    ANS = ANSRunner(resource, redisKey, logId, verbosity=4)
                else:
                    ANS = ANSRunner(resource, redisKey, logId)

                ANS.run_model(host_list=sList, module_name=model, module_args=args)
                Redis_pool.lpush(redisKey, "[Done] Ansible Done.")
                return JsonResponse({'msg': "操作成功", "code": 200, 'data': []})
            else:
                # print "操作失败，未选择主机或者该分组没有成员"
                return JsonResponse({'msg': "操作失败，未选择主机或者该分组没有成员", "code": 500, 'data': []})

    else:
        form = MoudelForm()
        rediskey = uuid.uuid4()
        return render(request, "deploy/moudel.html", locals())


@login_required
@permission_verify()
def scripts_list(request):
    if request.method == "GET":
        data_list = Ansible_Script.objects.all()
        for d in data_list:
            with open(os.getcwd() + str(d.script_file), 'r') as f:
                d.detail = ''.join(i for i in f.readlines())
        return render(request, "deploy/ansible_scripts_list.html", locals())


@login_required
@permission_verify()
def scripts_add(request):
    if request.method == "GET":
        form = ScriptsForm()
        uuidkey = uuid.uuid4()
        return render(request, "deploy/scripts_run_online.html", locals())
    elif request.method == "POST":
        scripts_uuid = request.POST.get('uuidkey')
        form = ScriptsForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            scripts_args = form.cleaned_data['scripts_args']
            debug = form.cleaned_data['_debug']
            inventory = form.cleaned_data['inventory']
            # print model,args,debug,inventory
            resource, sList = get_json_inentory(inventory.id, pw="get")

            def saveScript(content, filePath):
                if os.path.isdir(os.path.dirname(filePath)) is not True:
                    os.makedirs(os.path.dirname(filePath))  # 判断文件存放的目录是否存在，不存在就创建
                with open(filePath, 'w') as f:
                    f.write(content)
                return filePath

            if len(sList) > 0 and request.POST.get('type') == 'run':
                filePath = saveScript(content=request.POST.get('script_file'),
                                      filePath='/tmp/script-{ram}'.format(
                                          ram=uuid.uuid4().hex[0:8]))

                redisKey = scripts_uuid
                logId = AnsibleRecord.Model.insert(user=str(request.user), ans_model='script',
                                                   ans_server=','.join(sList), ans_args=filePath)
                Redis_pool.delete(redisKey)
                Redis_pool.lpush(redisKey,
                                 "[Start] Ansible Model: {model}  Script:{filePath} {args}".format(
                                     model='script', filePath=filePath, args=scripts_args))
                if debug == 'on':
                    ANS = ANSRunner(resource, redisKey, logId, verbosity=4)
                else:
                    ANS = ANSRunner(resource, redisKey, logId)
                ANS.run_model(host_list=sList, module_name='script',
                              module_args="{filePath} {args}".format(filePath=filePath,
                                                                     args=scripts_args))
                Redis_pool.lpush(redisKey, "[Done] Ansible Done.")
                try:
                    os.remove(filePath)
                except Exception, ex:
                    # logger.warn(msg="删除文件失败: {ex}".format(ex=ex))
                    print "删除文件失败: {ex}".format(ex=ex)
                return JsonResponse({'msg': "操作成功", "code": 200, 'data': []})
            elif request.POST.get('type') == 'save':
                fileName = '/upload/scripts/script-{ram}'.format(ram=uuid.uuid4().hex[0:8])
                filePath = os.getcwd() + fileName

                saveScript(content=request.POST.get('script_file'), filePath=filePath)
                try:
                    Ansible_Script.objects.create(
                        script_name=name,
                        script_uuid=scripts_uuid,
                        script_args=scripts_args,
                        script_server=json.dumps(sList),
                        script_group=inventory.id,
                        script_file=fileName,
                        # script_service=service,
                        # script_type=request.POST.get('server_model')
                    )
                except Exception, ex:
                    # logger.warn(msg="添加ansible脚本失败: {ex}".format(ex=ex))
                    return JsonResponse({'msg': str(ex), "code": 500, 'data': []})
                return JsonResponse({'msg': "保存成功", "code": 200, 'data': []})

            else:
                # print "操作失败，未选择主机或者该分组没有成员"
                return JsonResponse({'msg': "操作失败，未选择主机或者该分组没有成员",
                                     "code": 500, 'data': []})


@login_required
@permission_verify()
def scripts_run(request, s_id):
    if request.method == "GET":
        scripts = Ansible_Script.objects.get(id=s_id)
        uuidkey = scripts.script_uuid
        data = {'name': scripts.script_name,
                'inventory': scripts.script_group,
                'scripts_args': scripts.script_args,
                '_debug': 'off'}
        with open(os.getcwd() + str(scripts.script_file), 'r') as f:
            contents = '\n'.join(i for i in f.readlines())
        form = ScriptsForm(data)

        return render(request, "deploy/scripts_run_online.html", locals())


@login_required
@permission_verify()
def scripts_del(request, s_id):
    if request.method == "GET":
        scripts = Ansible_Script.objects.get(id=s_id)
        scripts.delete()
        data_list = Ansible_Script.objects.all()
        for d in data_list:
            with open(os.getcwd() + str(d.script_file), 'r') as f:
                d.detail = ''.join(i for i in f.readlines())
        return render(request, "deploy/ansible_scripts_list.html", locals())


@login_required
@permission_verify()
def playbook_del(request, s_id):
    if request.method == "GET":
        playbook = Ansible_Playbook.objects.get(id=s_id)
        playbook.delete()
        data_list = Ansible_Playbook.objects.all()
        for d in data_list:
            with open(os.getcwd() + str(d.playbook_file), 'r') as f:
                d.detail = ''.join(i for i in f.readlines())
        return render(request, "deploy/ansible_playbook_list.html", locals())


@login_required
@permission_verify()
def playbook_run(request, s_id):
    if request.method == "GET":
        playbook = Ansible_Playbook.objects.get(id=s_id)
        uuidkey = playbook.playbook_uuid
        data = {'name': playbook.playbook_name,
                'playbook_desc': playbook.playbook_desc,
                'inventory': playbook.playbook_auth_group,
                'playbook_args': playbook.playbook_vars,
                '_debug': 'off'}
        with open(os.getcwd() + str(playbook.playbook_file), 'r') as f:
            contents = '\n'.join(i for i in f.readlines())
        form = ScriptsForm(data)

        return render(request, "deploy/playbook_run_online.html", locals())


@login_required
@permission_verify()
def playbook_add(request):
    if request.method == "GET":
        form = PlaybookForm()
        uuidkey = uuid.uuid4()
        return render(request, "deploy/playbook_run_online.html", locals())
    elif request.method == "POST":
        playbook_uuid = request.POST.get('uuidkey')
        form = PlaybookForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            playbook_args = form.cleaned_data['playbook_args']
            playbook_desc = form.cleaned_data['playbook_desc']
            debug = form.cleaned_data['_debug']
            inventory = form.cleaned_data['inventory']
            # print name,playbook_args,playbook_desc,debug,inventory
            resource, sList = get_json_inentory(inventory.id, pw="get")

            def saveScript(content, filePath):
                if os.path.isdir(os.path.dirname(filePath)) is not True:
                    os.makedirs(os.path.dirname(filePath))  # 判断文件存放的目录是否存在，不存在就创建
                with open(filePath, 'w') as f:
                    f.write(content)
                return filePath

            if len(sList) > 0 and request.POST.get('type') == 'run':
                if Redis_pool.get(redisKey=playbook_uuid + '-locked') is None:
                    # 判断剧本是否有人在执行
                    # 加上剧本执行锁
                    Redis_pool.set(redisKey=playbook_uuid + '-locked', value=request.user)
                    # 删除旧的执行消息
                    Redis_pool.delete(playbook_uuid)
                    try:
                        if len(playbook_args) == 0:
                            playbook_args = dict()
                        else:
                            playbook_args = json.loads(playbook_args)
                        playbook_args['host'] = sList
                        filePath = None
                        fileobj = request.FILES.get("playbook_file_upload", None)
                        if fileobj:
                            filePath = os.path.join(os.getcwd(), 'upload/playbook', fileobj.name)
                            # if os.path.isdir(os.path.dirname(filename)) is not True:
                            if not os.path.exists(os.path.join(os.getcwd(), 'upload/playbook')):
                                # print("dir not exists,make it")
                                os.makedirs(os.path.join(os.getcwd(), 'upload/playbook'))
                            try:
                                with open(filePath, 'wb') as f:
                                    for chunk in fileobj.chunks():
                                        f.write(chunk)
                            except Exception as e:
                                print e
                        elif request.POST.get("playbook_file", None):
                            filePath = saveScript(content=request.POST.get('playbook_file'),
                                                  filePath='/tmp/playbook-{ram}'.format(
                                                      ram=uuid.uuid4().hex[0:8]))

                        logId = AnsibleRecord.PlayBook.insert(user=str(request.user),
                                                              # ans_id=playbook.id,
                                                              ans_name=name,
                                                              ans_content="执行Ansible剧本",
                                                              ans_server=','.join(sList))
                        # 执行ansible playbook
                        if request.POST.get('ansible_debug') == 'on':
                            ANS = ANSRunner(resource, redisKey=playbook_uuid, logId=logId, verbosity=4)
                        else:
                            ANS = ANSRunner(resource, redisKey=playbook_uuid, logId=logId)
                        if filePath:
                            ANS.run_playbook(host_list=sList, playbook_path=filePath,
                                             extra_vars=playbook_args)
                        # 获取结果
                        result = ANS.get_playbook_result()
                        dataList = []
                        statPer = {
                            "unreachable": 0,
                            "skipped": 0,
                            "changed": 0,
                            "ok": 0,
                            "failed": 0
                        }
                        for k, v in result.get('status').items():
                            v['host'] = k
                            if v.get('failed') > 0 or v.get('unreachable') > 0:
                                v['result'] = 'Failed'
                            else:
                                v['result'] = 'Succeed'
                            dataList.append(v)
                            statPer['unreachable'] = v['unreachable'] + statPer['unreachable']
                            statPer['skipped'] = v['skipped'] + statPer['skipped']
                            statPer['changed'] = v['changed'] + statPer['changed']
                            statPer['failed'] = v['failed'] + statPer['failed']
                            statPer['ok'] = v['ok'] + statPer['ok']
                        Redis_pool.lpush(playbook_uuid, "[Done] Ansible Done.")
                        return JsonResponse({'msg': "操作成功", "code": 200, 'data': dataList, "statPer": statPer})
                    except Exception as e:
                        return JsonResponse({'msg': "剧本执行失败，{}".format(e), "code": 500,
                                             'data': []})
                    finally:
                        # 切换版本之后取消项目部署锁
                        Redis_pool.delete(redisKey=playbook_uuid + '-locked')



                else:
                    return JsonResponse({'msg': "剧本执行失败，{user}正在执行该剧本".format(
                        user=Redis_pool.get(playbook_uuid + '-locked')), "code": 500,
                        'data': []})





            elif request.POST.get('type') == 'save':
                fileobj = request.FILES.get("playbook_file_upload", None)
                fileName = None
                if fileobj:
                    fileName = os.path.join('/upload/playbook', fileobj.name)
                    filePath = os.path.join(os.getcwd(), 'upload/playbook', fileobj.name)
                    # if os.path.isdir(os.path.dirname(filename)) is not True:
                    if not os.path.exists(os.path.join(os.getcwd(), 'upload/playbook')):
                        # print("dir not exists,make it")
                        os.makedirs(os.path.join(os.getcwd(), 'upload/playbook'))
                    try:
                        with open(filePath, 'wb') as f:
                            for chunk in fileobj.chunks():
                                f.write(chunk)
                    except Exception as e:
                        print e
                elif request.POST.get("playbook_file", None):

                    fileName = '/upload/playbook/playbook-{name}-{ram}'.format(name=name,
                                                                               ram=uuid.uuid4().hex[0:8])
                    filePath = os.getcwd() + fileName

                    saveScript(content=request.POST.get('playbook_file'), filePath=filePath)
                try:
                    defaults = {
                        'playbook_name': name,
                        'playbook_uuid': playbook_uuid,
                        'playbook_vars': playbook_args,
                        'playbook_desc': playbook_desc,
                        'playbook_auth_group': inventory.id,
                        'playbook_file': fileName,
                    }
                    Ansible_Playbook.objects.update_or_create(
                        playbook_name=name, defaults=defaults)
                    return JsonResponse({'msg': "保存成功", "code": 200, 'data': []})
                except Exception, ex:
                    # logger.warn(msg="添加ansible脚本失败: {ex}".format(ex=ex))
                    return JsonResponse({'msg': str(ex), "code": 500, 'data': []})


            else:
                # print "操作失败，未选择主机或者该分组没有成员"
                return JsonResponse({'msg': "操作失败，未选择主机或者该分组没有成员",
                                     "code": 500, 'data': []})


@login_required
@permission_verify()
def playbook_list(request):
    if request.method == "GET":
        data_list = Ansible_Playbook.objects.all()
        for d in data_list:
            with open(os.getcwd() + str(d.playbook_file), 'r') as f:
                d.detail = ''.join(i for i in f.readlines())
        return render(request, "deploy/ansible_playbook_list.html", locals())


@login_required
@permission_verify()
def ansible_log(request):
    if request.method == "GET":
        modelList = Log_Ansible_Model.objects.all().order_by('-id')[0:500]
        playbookList = Log_Ansible_Playbook.objects.all().order_by('-id')[0:500]
        return render(request, "deploy/ansible_log.html", locals())


@login_required
@permission_verify()
def ansible_log_view(request, s_id):
    if request.method == "GET":
        data = "未找到相关信息！"
        if request.GET.get("m_p") == "moudel" or request.GET.get("m_p") == "model":
            data = Log_Ansible_Model.objects.get(id=s_id).ansible_model_log.all()[0].content
        elif request.GET.get("m_p") == "playbook":
            data = Log_Ansible_Playbook.objects.get(id=s_id).ansible_playbook_log.all()[0].content
        return JsonResponse({'data': data})


@login_required
@permission_verify()
def ansible_log_del(request, s_id):
    if request.method == "GET":
        if request.GET.get("m_p") == "moudel" or request.GET.get("m_p") == "model":
            Log_Ansible_Model.objects.get(id=s_id).delete()
        elif request.GET.get("m_p") == "playbook":
            Log_Ansible_Playbook.objects.get(id=s_id).delete()
        return JsonResponse({'messages': '删除成功！'})
