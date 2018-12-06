# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os
import uuid

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# from .base import GitTools,SvnTools
import base
from accounts.permission import permission_verify
from cmdb.models import Server_asset
from deploy.ansible_api_v2 import ANSRunner
from .forms import ProjectForm
from .models import *
from .redis_ops_delivery import OpsProject
from .tasks import recordProject

logger = logging.getLogger('django.delivery')


# Create your views here.
@login_required(login_url="/login/")
@permission_verify()
def delivery_list(request):
    if request.method == "GET":
        user_name = request.user
        data_list = Project_Config.objects.all()
        for data in data_list:
            data.server = ','.join(i.server for i in data.project_number.all())
        return render(request, 'delivery/delivery_list.html', locals())


@login_required(login_url="/login/")
@permission_verify()
def delivery_add(request):
    user_name = request.user
    if request.method == "GET":
        form = ProjectForm()
        return render(request, 'delivery/delivery_add.html', locals())
    elif request.method == "POST":
        form = ProjectForm(request.POST)
        ipList = request.POST.getlist("server", [])
        # ipList = request.POST.get("server")
        if form.is_valid():
            proj = form.save(commit=False)
            proj.project_uuid = uuid.uuid4()
            proj.save()
            # form.save_m2m() # 保存多对多的时候才使用

            if ipList:
                for sid in ipList:
                    # for sid in ipList.split(','):
                    try:
                        assets = Server_asset.objects.get(id=sid)

                        Project_Number.objects.create(dir=request.POST.get('project_dir'),
                                                      server=assets.ip, project=proj)
                    except Exception as ex:
                        proj.delete()
                        # logger.error(msg="部署项目添加失败: {ex}".format(ex=ex))
                        message = "新增失败,%s" % ex
                        return render(request, 'delivery/delivery_add.html', locals())

            message = "新增成功"
            return render(request, 'delivery/delivery_add.html', locals())
        message = "新增失败"
        return render(request, 'delivery/delivery_add.html', locals())


@login_required(login_url="/login/")
@permission_verify()
def delivery_edit(request, pid):
    user_name = request.user
    project_data = Project_Config.objects.get(id=pid)
    if request.method == "GET":
        form = ProjectForm(instance=project_data)
        return render(request, 'delivery/delivery_edit.html', locals())
    elif request.method == "POST":
        form = ProjectForm(request.POST, instance=project_data)
        ipList = request.POST.getlist("server", [])
        # ipList = request.POST.get("server")
        if form.is_valid():
            proj = form.save()

            if ipList:
                for sid in ipList:
                    # for sid in ipList.split(','):
                    try:
                        assets = Server_asset.objects.get(id=sid)
                        default = {'dir': request.POST.get('project_dir'),
                                   'server': assets.ip, 'project': proj}
                        Project_Number.objects.update_or_create(defaults=default,
                                                                server=assets.ip, project=proj)
                    except Exception as ex:
                        proj.delete()
                        # logger.error(msg="部署项目添加失败: {ex}".format(ex=ex))
                        message = "新增失败,%s" % ex
                        return render(request, 'delivery/delivery_edit.html', locals())

            message = "新增成功"
            return render(request, 'delivery/delivery_edit.html', locals())
        message = "新增失败"
        return render(request, 'delivery/delivery_edit.html', locals())


@login_required(login_url="/login/")
@permission_verify()
def delivery_log(request):
    if request.method == "GET":
        user_name = request.user
        data_list = Log_Project_Config.objects.all().order_by('-id')[0:100]
        for data in data_list:
            try:
                data.project=Project_Config.objects.get(id=data.project_id)
            except Exception as ex:
                logger.info(msg="项目id: {ex}可能已经被删除了".format(ex=ex))
        return render(request, 'delivery/delivery_log.html', locals())




@login_required(login_url="/login/")
@permission_verify()
def delivery_del(request, id):
    if request.method == "GET":
        Project_Config.objects.get(id=id).delete()
        user_name = request.user
        data_list = Project_Config.objects.all()
        return render(request, 'delivery/delivery_list.html', locals())


@login_required(login_url="/login/")
@permission_verify()
def delivery_init(request, pid):
    if request.method == "POST":
        project = Project_Config.objects.select_related().get(id=pid)
        if project.project_repertory == 'git':
            version = base.GitTools()
        elif project.project_repertory == 'svn':
            version = base.SvnTools()
        version.mkdir(dir=project.project_repo_dir)
        if project.project_type == 'compile': version.mkdir(dir=project.project_dir)
        result = version.clone(url=project.project_address, dir=project.project_repo_dir,
                               user=project.project_repo_user, passwd=project.project_repo_passwd)
        if result[0] > 0:
            return JsonResponse({'msg': result[1], "code": 500, 'data': []})
        else:
            Project_Config.objects.filter(id=pid).update(project_status=1)
            # recordProject.delay(project_user=str(request.user), project_id=project.id,
            #                     project_name=project.project_name, project_content="初始化项目")
            return JsonResponse({'msg': "初始化成功", "code": 200, 'data': []})


@login_required(login_url="/login/")
@permission_verify()
def delivery_version(request, pid):
    try:
        project = Project_Config.objects.select_related().get(id=pid)
        if project.project_repertory == 'git': version = base.GitTools()
    except:
        return render(request, 'deploy/deploy_version.html', {"user": request.user,
                                                              "errorInfo": "项目不存在，可能已经被删除."},
                      )
    if request.method == "POST":
        try:
            project = Project_Config.objects.get(id=pid)
            if project.project_repertory == 'git':
                version = base.GitTools()
            elif project.project_repertory == 'svn':
                version = base.SvnTools()
        except:
            return JsonResponse({'msg': "项目资源不存在", "code": 403, 'data': []})
        if project.project_status == 0: return JsonResponse({'msg': "请先初始化项目", "code": 403, 'data': []})
        if request.POST.get('op') in ['create', 'delete', 'query', 'histroy']:
            if request.POST.get('op') == 'create':
                if request.POST.get('model') == 'branch':
                    result = version.createBranch(path=project.project_repo_dir, branchName=request.POST.get('name'))
                elif request.POST.get('model') == 'tag':
                    result = version.createTag(path=project.project_repo_dir, tagName=request.POST.get('name'))
            elif request.POST.get('op') == 'delete':
                if request.POST.get('model') == 'branch':
                    result = version.delBranch(path=project.project_repo_dir, branchName=request.POST.get('name'))
                elif request.POST.get('model') == 'tag':
                    result = version.delTag(path=project.project_repo_dir, tagName=request.POST.get('name'))
            elif request.POST.get('op') == 'query':
                if project.project_model == 'branch':
                    result = version.log(path=project.project_repo_dir, bName=request.POST.get('name'), number=50)
                    return JsonResponse({'msg': "操作成功", "code": 200, 'data': result})
                else:
                    result = version.tag(path=project.project_repo_dir)
            elif request.POST.get('op') == 'histroy':
                result = version.show(path=project.project_repo_dir, branch=request.POST.get('project_branch'),
                                      cid=request.POST.get('project_version', None))
                return JsonResponse({'msg': "操作成功", "code": 200,
                                     'data': "<pre> <xmp>" + result[1].replace('<br>', '\n') + "</xmp></pre>"})
        else:
            return JsonResponse({'msg': "非法操作", "code": 500, 'data': []})
        if result[0] > 0:
            return JsonResponse({'msg': result[1], "code": 500, 'data': []})
        else:
            return JsonResponse({'msg': "操作成功", "code": 200, 'data': []})


@login_required()
def delivery_result(request,pid):
    if request.method == "POST":
        msg = OpsProject.rpop(request.POST.get('project_uuid'))
        if msg:return JsonResponse({'msg':msg,"code":200,'data':[]})
        else:return JsonResponse({'msg':None,"code":200,'data':[]})


@login_required(login_url="/login/")
@permission_verify()
def delivery_run(request, pid):
    try:
        project = Project_Config.objects.get(id=pid)
        serverList = Project_Number.objects.filter(project=project)
        if project.project_repertory == 'git':
            version = base.GitTools()
        elif project.project_repertory == 'svn':
            version = base.SvnTools()
    except Exception, ex:
        logger.error(msg="项目部署失败: {ex}".format(ex=ex))
        return render(request, 'delivery/delivery_run.html', {"user": request.user,
                                                              "errorInfo": "项目部署失败: {ex}".format(ex=ex)},
                      )
    if request.method == "GET":
        if project.project_model == 'branch':
            bList = version.branch(path=project.project_repo_dir)
        elif project.project_model == 'tag':
            bList = version.tag(path=project.project_repo_dir)
        else:
            bList = version.trunk(path=project.project_repo_dir)
        if project.project_env == 'uat':
            return render(request, 'delivery/delivery_run.html', {"user": request.user,
                                                                  "project": project, "serverList": serverList,
                                                                  "errorInfo": "正式环境代码部署，请走工单审批流程"},
                          )
            # 获取最新版本
        version.pull(path=project.project_repo_dir)
        vList = version.log(path=project.project_repo_dir, number=50)
        return render(request, 'delivery/delivery_run.html', {"user": request.user,
                                                              "project": project, "serverList": serverList,
                                                              "bList": bList, "vList": vList, },
                      )

    elif request.method == "POST":
        if request.POST.getlist('project_server', None):
            serverList = [Project_Number.objects.get(project=project, server=ds) for ds in
                          request.POST.getlist('project_server')]
            allServerList = [ds.server for ds in Project_Number.objects.filter(project=project)]
            # 获取项目目标服务器列表与分批部署服务器（post提交）列表的差集
            tmpServer = [i for i in allServerList if i not in request.POST.getlist('project_server')]
        elif request.POST.get('project_model', None) == "rollback":
            tmpServer = None
        else:
            return JsonResponse({'msg': "项目部署失败：未选择目标服务器", "code": 500, 'data': []})

        # OpsProject.delete(redisKey=project.project_uuid + "-locked")
        if OpsProject.get(redisKey=project.project_uuid + "-locked") is None:  # 判断该项目是否有人在部署
            # 给项目部署加上锁
            OpsProject.set(redisKey=project.project_uuid + "-locked", value=request.user)
            OpsProject.delete(project.project_uuid)
            if request.POST.get('project_model', None) == "rollback":
                project_content = "回滚项目"
                if project.project_model == 'branch':
                    verName = request.POST.get('project_version')
                    trueDir = project.project_dir + project.project_env + '/' + request.POST.get(
                        'project_version') + '/'
                    OpsProject.lpush(project.project_uuid, data="[PULL] Start Rollback branch:%s  vesion: %s" % (
                        request.POST.get('project_branch'), request.POST.get('project_version')))
                elif project.project_model == 'tag':
                    verName = request.POST.get('project_branch')
                    trueDir = project.project_dir + project.project_env + '/' + request.POST.get('project_branch') + '/'
                    OpsProject.lpush(project.project_uuid,
                                     data="[PULL] Start Rollback tag:%s" % request.POST.get('project_branch'))
                # 创建版本目录
                base.mkdir(dirPath=trueDir)
                OpsProject.lpush(project.project_uuid,
                                 data="[PULL] Mkdir version dir: {dir} ".format(dir=trueDir))
                # 创建快捷方式
                softdir = project.project_dir + project.project_name + '/'
                result = base.lns(spath=trueDir, dpath=softdir.rstrip('/'))
                OpsProject.lpush(project.project_uuid,
                                 data="[PULL] Make softlink cmd:  ln -s  {sdir} {ddir} info: {info}".format(
                                     sdir=trueDir, ddir=softdir, info=result[1]))
                if result[0] > 0: return JsonResponse({'msg': result[1], "code": 500, 'data': []})
                # 获取要排除的文件
                exclude = None
                if project.project_exclude:
                    try:
                        exclude = ''
                        for s in project.project_exclude.split(','):
                            exclude = "--exclude='{file}'".format(
                                file=s.replace('\r\n', '').replace('\n', '').strip()) + ' ' + exclude
                    except Exception, e:
                        return JsonResponse({'msg': str(e), "code": 500, 'data': []})
                #todo 回滚没写完
            else:
                OpsProject.lpush(project.project_uuid, data="[PULL start get code on server]")
                project_content = "部署项目"
                # 判断版本上线类型再切换分支到指定的分支/Tag
                if project.project_model == 'branch' or project.project_repertory == 'svn':
                    bName = request.POST.get('project_branch')
                    result = version.checkOut(path=project.project_repo_dir, name=bName)
                    OpsProject.lpush(project.project_uuid, data="[PULL] Switched to branch %s" % bName)
                    # reset到指定版本
                    result = version.reset(path=project.project_repo_dir, commintId=request.POST.get('project_version'))
                    OpsProject.lpush(project.project_uuid,
                                     data="[PULL] Git reset to {comid} info: {info}".format(
                                         comid=request.POST.get('project_version'), info=result[1]))
                    trueDir = project.project_dir + project.project_env + '/' + request.POST.get(
                        'project_version') + '/'
                    verName = bName + '_' + request.POST.get('project_version', '未知')
                elif project.project_model == 'tag':
                    bName = request.POST.get('project_branch')
                    result = version.checkOut(path=project.project_repo_dir, name=bName)
                    OpsProject.lpush(project.project_uuid, data="[PULL] Switched to tag %s" % bName)
                    trueDir = project.project_dir + project.project_env + '/' + bName + '/'
                    verName = bName
                # 创建版本目录
                base.mkdir(dirPath=trueDir)
                OpsProject.lpush(project.project_uuid,
                                 data="[PULL] Mkdir version dir: {dir} ".format(dir=trueDir))
                # 创建快捷方式
                softdir = project.project_dir + project.project_name + '/'
                result = base.lns(spath=trueDir, dpath=softdir.rstrip('/'))
                OpsProject.lpush(project.project_uuid,
                                 data="[PULL] Make softlink cmd:  ln -s  {sdir} {ddir} info: {info}".format(
                                     sdir=trueDir, ddir=softdir, info=result[1]))
                if result[0] > 0: return JsonResponse({'msg': result[1], "code": 500, 'data': []})
                # 获取要排除的文件
                exclude = None
                if project.project_exclude:
                    try:
                        exclude = ''
                        for s in project.project_exclude.split(','):
                            exclude = "--exclude='{file}'".format(
                                file=s.replace('\r\n', '').replace('\n', '').strip()) + ' ' + exclude
                    except Exception, e:
                        return JsonResponse({'msg': str(e), "code": 500, 'data': []})
                        # 执行部署命令  - 编译型语言
                if project.project_local_command and project.project_type == 'compile':
                    tmpFile = '/tmp/' + uuid.uuid4().hex[0:8] + '.sh'
                    with open(tmpFile, 'w') as f:
                        f.write(project.project_local_command)
                    OpsProject.lpush(project.project_uuid, data="[DEPLOY start deploy project]")
                    OpsProject.lpush(project.project_uuid,
                                     data="[DEPLOY] try to converting deploy scripts file {tmpFile}".format(
                                         tmpFile=tmpFile))
                    result = base.cmds(cmds='dos2unix {tmpFile}'.format(tmpFile=tmpFile))
                    OpsProject.lpush(project.project_uuid, data="[DEPLOY] {cmds} info: {info}".format(
                        cmds='dos2unix {tmpFile}'.format(tmpFile=tmpFile), info=result[1]))
                    result = base.cmds(cmds='cd {project_repo_dir} && bash {tmpFile}'.format(tmpFile=tmpFile,
                                                                                             project_repo_dir=project.project_repo_dir))
                    os.remove(tmpFile)
                    OpsProject.lpush(project.project_uuid,
                                     data="[DEPLOY] Execute deploy scripts: {cmds} <br>{info}".format(
                                         cmds='bash {tmpFile}'.format(tmpFile=tmpFile),
                                         info=result[1].replace('\n', '<br>')))
                    if result[0] > 0: return JsonResponse({'msg': result[1], "code": 500, 'data': []})
                    OpsProject.lpush(project.project_uuid, data="[Pack start package project]")
                    # 非编译型语言
                else:
                    OpsProject.lpush(project.project_uuid, data="[Pack start package project]")
                    # 配置rsync同步文件到本地目录
                    result = base.rsync(sourceDir=project.project_repo_dir, destDir=trueDir, exclude=exclude)
                    OpsProject.lpush(project.project_uuid,
                                     data="[Pack] Rsync {sDir} to {dDir} exclude {exclude}".format(
                                         sDir=project.project_repo_dir, dDir=trueDir, exclude=exclude))
                    if result[0] > 0: return JsonResponse({'msg': result[1], "code": 500, 'data': []})
                    # 授权文件
                result = base.chown(user=project.project_user, path=trueDir)
                OpsProject.lpush(project.project_uuid,
                                 data="[Pack] Chown {user} to {path}".format(user=project.project_user,
                                                                             path=trueDir))
                if result[0] > 0: return JsonResponse({'msg': result[1], "code": 500, 'data': []})
                # 调用ansible同步代码到远程服务器上
            resource = []
            hostList = []
            for ds in serverList:
                server = Server_asset.objects.get(ip=ds.server)
                hostList.append(ds.server)
                data = dict()
                # if len(server.keyfile) == 0: data["password"] = server.passwd
                data["password"] = server.passwd
                data["ip"] = server.ip
                if server.port: data["port"] = int(server.port)
                data["username"] = server.username
                if server.sudo_passwd: data["sudo_passwd"] = server.sudo_passwd
                resource.append(data)
            OpsProject.lpush(project.project_uuid, data="[RSYNC start rsync project to remote server]")
            if resource and hostList:
                if exclude:
                    args = '''src={srcDir} dest={desDir} links=yes recursive=yes compress=yes delete=yes rsync_opts="{exclude}"'''.format(
                        # srcDir=softdir, desDir=ds.dir, exclude=exclude)
                        srcDir=softdir, desDir='/var/www/remote/test1/', exclude=exclude) #同一台机器测试，远程目录暂用临时目录
                else:
                    args = '''src={srcDir} dest={desDir} links=yes recursive=yes compress=yes delete=yes'''.format(
                        # srcDir=softdir, desDir=ds.dir)
                        srcDir=softdir, desDir='/var/www/remote/test1/')  # 同一台机器测试，远程目录暂用临时目录
                ANS = ANSRunner(resource)
                ANS.run_model(host_list=hostList, module_name='synchronize', module_args=args)
                # 精简返回的结果
                dataList = ANS.handle_model_data(ANS.get_model_result(), 'synchronize', module_args=args)
                for ds in dataList:
                    OpsProject.lpush(project.project_uuid,
                                     data="[RSYNC] Rsync project to {host} status: {status} msg: {msg}".format(
                                         host=ds.get('ip'),
                                         status=ds.get('status'),
                                         msg=ds.get('msg')))
                    if ds.get('status') == 'failed': result = (1, ds.get('ip') + ds.get('msg'))
            # 目标服务器执行后续命令
            if project.project_remote_command:
                OpsProject.lpush(project.project_uuid, data="[CMD start run command to remote server]")
                ANS.run_model(host_list=hostList, module_name='raw', module_args=project.project_remote_command)
                # 精简返回的结果
                dataList = ANS.handle_model_data(ANS.get_model_result(), 'raw',
                                                 module_args=project.project_remote_command)
                for ds in dataList:
                    OpsProject.lpush(project.project_uuid,
                                     data="[CMD] Execute command to {host} status: {status} msg: {msg}".format(
                                         host=ds.get('ip'),
                                         status=ds.get('status'),
                                         msg=ds.get('msg')))
                    if ds.get('status') == 'failed': result = (1, "部署错误: " + ds.get('msg'))
            if result[0] > 0:
                OpsProject.delete(redisKey=project.project_uuid + "-locked")
                return JsonResponse({'msg': result[1], "code": 500, 'data': []})
            OpsProject.lpush(project.project_uuid, data="[Done] Deploy Success.")
            # 切换版本之后取消项目部署锁
            OpsProject.delete(redisKey=project.project_uuid + "-locked")
            # 异步记入操作日志
            #             if request.POST.get('project_version'):bName = request.POST.get('project_version')
            recordProject.delay(project_user=str(request.user), project_id=project.id,
                                project_name=project.project_name,
                                project_content=project_content,
                                project_branch=verName)
            return JsonResponse({'msg': "项目部署成功", "code": 200, 'data': tmpServer})
        else:
            return JsonResponse({'msg': "项目部署失败：{user}正在部署改项目，请稍后再提交部署。".format(
                user=OpsProject.get(redisKey=project.project_uuid + "-locked")), "code": 500, 'data': []})
