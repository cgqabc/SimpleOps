#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from forms import PermissionsForm
from models import User_info, RolueGroups, Permissions


def permission_verify():
    """
        权限认证模块,
        此模块会先判断用户是否是管理员（is_superuser为True），如果是管理员，则具有所有权限,
        如果不是管理员则获取request.user和request.path两个参数，判断两个参数是否匹配，匹配则有权限，反之则没有。
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            iUser = User_info.objects.get(username=request.user)
            # 判断用户如果是超级管理员则具有所有权限
            if not iUser.is_superuser:
                if not iUser.role:  # 如果用户无角色，直接返回无权限
                    return HttpResponseRedirect(reverse('permission_deny'))

                role_permission = RolueGroups.objects.get(name=iUser.role)
                role_permission_list = role_permission.permission.all()

                matchUrl = []
                for x in role_permission_list:
                    # 精确匹配，判断request.path是否与permission表中的某一条相符
                    # print request.path,x.url
                    if request.path == x.url or request.path.rstrip('/') == x.url:
                        matchUrl.append(x.url)
                    # 判断request.path是否以permission表中的某一条url开头
                    elif request.path.startswith(x.url):
                        matchUrl.append(x.url)
                    else:
                        pass

                print('{}---->matchUrl:{}'.format(request.user, str(matchUrl)))
                if len(matchUrl) == 0:
                    return HttpResponseRedirect(reverse('permission_deny'))
            else:
                pass

            return view_func(request, *args, **kwargs)
        return _wrapped_view

    return decorator


@login_required
def permission_deny(request):
    kwvars = {
        'request': request,
    }

    return render(request, 'accounts/permission_deny.html', kwvars)


@login_required
@permission_verify()
def permission_add(request):
    if request.method == "POST":
        form = PermissionsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('permission_list'))
    else:
        form = PermissionsForm()

    kwvars = {
        'form': form,
        'request': request,
    }

    return render(request, 'accounts/permission_add.html', kwvars)


@login_required
@permission_verify()
def permission_list(request):
    all_permission = Permissions.objects.all()
    return render(request, 'accounts/permission_list.html', locals())


@login_required
@permission_verify()
def permission_edit(request, ids):
    iPermission = Permissions.objects.get(id=ids)

    if request.method == "POST":
        form = PermissionsForm(request.POST, instance=iPermission)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('permission_list'))
    else:
        form = PermissionsForm(instance=iPermission)

    kwvars = {
        'ids': ids,
        'form': form,
        'request': request,
    }

    return render(request, 'accounts/permission_edit.html', kwvars)


@login_required
@permission_verify()
def permission_del(request, ids):
    Permissions.objects.filter(id=ids).delete()

    return HttpResponseRedirect(reverse('permission_list'))
