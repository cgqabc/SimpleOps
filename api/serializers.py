#! /usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from cmdb.models import Assets,Server_asset,Service_Assets,BusinessUnit

class AssetsSerializer(ModelSerializer):

    class Meta:
        model = Assets
        fields = ['asset_type','name','sn','status','manage_ip']


class ServerSerializer(ModelSerializer):

    class Meta:
        model = Server_asset
        fields = ['asset','ip']

# class ServiceSerializer(ModelSerializer):
#
#     class Meta:
#         model = Service_Assets
#         fields = ['id','business','service_name']
class ServiceSerializer(ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    project_id = serializers.IntegerField(source='project.id', read_only=True)

    class Meta:
        model = Service_Assets
        fields = ('id', 'service_name', 'project_name', 'project_id')


class ProjectSerializer(serializers.ModelSerializer):
    service_assets = ServiceSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = BusinessUnit
        fields = ('id', 'name', 'service_assets')