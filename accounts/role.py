#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from forms import RolueGroupsForm
from models import RolueGroups
from accounts.permission import permission_verify


@login_required
@permission_verify()
def role_add(request):
    if request.method == "POST":
        form = RolueGroupsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('role_list'))
    else:
        form = RolueGroupsForm()

    kwvars = {
        'form': form,
        'request': request,
    }

    return render(request, 'accounts/role_add.html', kwvars)


@login_required
@permission_verify()
def role_list(request):
    all_role = RolueGroups.objects.all()
    return render(request, 'accounts/role_list.html', {'all_role':all_role})


@login_required
@permission_verify()
def role_edit(request, ids):
    iRole = RolueGroups.objects.get(id=ids)
    temp_name = "accounts/accounts-header.html"
    if request.method == "POST":
        form = RolueGroupsForm(request.POST, instance=iRole)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('role_list'))
    else:
        form = RolueGroupsForm(instance=iRole)

    kwvars = {
        'temp_name': temp_name,
        'ids': ids,
        'form': form,
        'request': request,
    }

    return render(request, 'accounts/role_edit.html', kwvars)


@login_required
@permission_verify()
def role_del(request, ids):
    RolueGroups.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('role_list'))

