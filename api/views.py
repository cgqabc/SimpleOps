# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from accounts.permission import permission_verify
from .serializers import AssetsSerializer,ServerSerializer,ServiceSerializer,ProjectSerializer
from cmdb.models import Assets,Server_asset,Service_Assets,BusinessUnit
from rest_framework import status

# Create your views here.

@api_view(['GET','POST'])
@permission_verify()
def assets_list(request,format=None):
    if request.method == "GET":
        assets = Assets.objects.all()
        serializer = AssetsSerializer(assets,many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = AssetsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST',"DELETE"])
@permission_verify()
def assets_detail(request,id,format=None):
    try:
        asset = Assets.objects.get(id=id)
    except Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = AssetsSerializer(asset)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = AssetsSerializer(asset,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        asset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_verify()
def project_list(request, format=None):
    if request.method == 'GET':
        snippets = BusinessUnit.objects.all()
        serializer = ProjectSerializer(snippets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # recordAssets.delay(user=str(request.user),
            #                    content="添加产品线名称：{project_name}".format(project_name=request.data.get("project_name")),
            #                    type="project", id=serializer.data.get('id'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
@permission_verify()
def project_detail(request, id, format=None):
    try:
        snippet = BusinessUnit.objects.get(id=id)
    except BusinessUnit.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProjectSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProjectSerializer(snippet, data=request.data)
        old_name = snippet.project_name
        if serializer.is_valid():
            serializer.save()
            # recordAssets.delay(user=str(request.user),
            #                    content="修改产品线为：{old_name} -> {project_name}".format(
            # old_name=old_name,
            #                                                                         project_name=request.data.get(
            #                                                                             "project_name")),
            #                    type="project", id=id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE' :
        if not request.user.has_perm('OpsManage.can_delete_rroject_Assets'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST' ])
@permission_verify()
def service_list(request,format=None):
    if request.method == 'GET':
        snippets = Service_Assets.objects.all()
        serializer = ServiceSerializer(snippets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # del request.data['project_name']
        try:
            service = Service_Assets.objects.create(**request.data)
        except Exception, ex:
            return Response({"msg":str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        try:
            snippet = Service_Assets.objects.get(id=service.id)
            serializer = ServiceSerializer(snippet)
            # recordAssets.delay(user=str(request.user),content="添加业务类型名称：{service_name}".format(service_name=request.data.get("service_name")),type="service",id=serializer.data.get('id'))
        except Exception, ex:
            # logger.error(msg="添加service失败: {ex}".format(ex=str(ex)))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

@api_view(['GET','POST'])
@permission_verify()
def service_detail(request,id):
    try:
        service = Service_Assets.objects.get(id=id)
    except Service_Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = ServiceSerializer(service)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ServiceSerializer(service,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)