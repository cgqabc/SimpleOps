#! /usr/bin/env python
# -*- coding: utf-8 -*-
# !/usr/bin/env python
# _#_ coding:utf-8 _*_
from cmdb.models import Assets, Server_asset, Network_asset,BusinessUnit,Service_Assets
from .models import  Ansible_Inventory
import logging
logger=logging.getLogger('django.assets')


class AssetsSource(object):
    def __init__(self):
        super(AssetsSource, self).__init__()

    def serverList(self):
        serverList = []
        for assets in Assets.objects.filter(asset_type__in=["server", 'vmserver','netdevice']):
            try:
                service = assets.business_unit.service_assets.service_name
            except:
                service = '未知'
            try:
                project = assets.business_unit.name
            except:
                project = '未知'
            if hasattr(assets, 'server_asset'):
                serverList.append(
                    {"id": assets.id, "ip": assets.server_asset.ip, 'project': project, 'service': service})
            elif hasattr(assets, 'network_asset'):
                serverList.append(
                    {"id": assets.id, "ip": assets.network_asset.ip, 'project': project, 'service': service})
        return serverList

    def queryAssetsByIp(self, ipList):
        sList = []
        resource = []
        for ip in ipList:
            data = {}
            server = Server_asset.objects.filter(ip=ip).count()
            network = Network_asset.objects.filter(ip=ip).count()
            if server > 0:
                try:
                    server_assets = Server_asset.objects.get(ip=ip)
                    sList.append(server_assets.ip)
                    data["ip"] = server_assets.ip
                    data["port"] = int(server_assets.port)
                    data["username"] = server_assets.username
                    data["sudo_passwd"] = server_assets.sudo_passwd
                    if server_assets.keyfile != 1: data["password"] = server_assets.passwd
                except Exception, ex:
                    logger.warn(msg="server_id:{assets}, error:{ex}".format(assets=server_assets.id, ex=ex))
                if server_assets.assets.host_vars:
                    try:
                        for k, v in eval(server_assets.assets.host_vars).items():
                            if k not in ["ip", "port", "username", "password", "ip"]: data[k] = v
                    except Exception, ex:
                        logger.warn(msg="资产: {assets},转换host_vars失败:{ex}".format(assets=server_assets.assets.id, ex=ex))
            elif network > 0:
                try:
                    network_assets = Network_asset.objects.get(ip=ip)
                    sList.append(network_assets.ip)
                    data["ip"] = network_assets.ip
                    data["port"] = int(network_assets.port)
                    data["password"] = network_assets.passwd,
                    data["username"] = network_assets.username
                    data["sudo_passwd"] = network_assets.sudo_passwd
                    data["connection"] = 'local'
                except Exception, ex:
                    logger.warn(msg="network_id:{assets}, error:{ex}".format(assets=server_assets.id, ex=ex))
                if network_assets.assets.host_vars:
                    try:
                        for k, v in eval(network_assets.assets.host_vars).items():
                            if k not in ["ip", "port", "username", "password", "ip"]: data[k] = v
                    except Exception, ex:
                        logger.warn(
                            msg="资产: {assets},转换host_vars失败:{ex}".format(assets=network_assets.assets.id, ex=ex))
            resource.append(data)
        return sList, resource

    def custom(self, serverList):
        assetsList = []
        for server in serverList:
            try:
                assetsList.append(Assets.objects.select_related().get(id=server))
            except:
                pass
        return self.source(assetsList)

    def group(self, group):
        assetsList = Assets.objects.select_related().filter(group=group,
                                                            asset_type__in=["server", 'vmserver','netdevice'])
        return self.source(assetsList)

    def service(self, business):
        assetsList = Assets.objects.select_related().filter(business_unit__id=business,
                                                            asset_type__in=["server", 'vmserver','netdevice'])
        return self.source(assetsList)

    def source(self, assetsList):
        sList = []
        resource = []
        for assets in assetsList:
            data = {}
            if hasattr(assets, 'server_asset'):
                try:
                    sList.append(assets.server_asset.ip)
                    data["ip"] = assets.server_asset.ip
                    if assets.server_asset.port: data["port"] = int(assets.server_asset.port)
                    data["username"] = assets.server_asset.username
                    data["sudo_passwd"] = assets.server_asset.sudo_passwd
                    # if assets.server_asset.keyfile == 0: data["password"] = assets.server_asset.passwd
                    data["password"] = assets.server_asset.passwd
                except Exception, ex:
                    logger.warn(msg="id:{assets}, error:{ex}".format(assets=assets.id, ex=ex))
            elif hasattr(assets, 'network_asset'):
                try:
                    sList.append(assets.network_asset.ip)
                    if assets.server_asset.port: data["ip"] = assets.network_asset.ip
                    data["port"] = int(assets.network_asset.port)
                    data["password"] = assets.network_asset.passwd,
                    data["username"] = assets.network_asset.username
                    data["sudo_passwd"] = assets.network_asset.sudo_passwd
                    data["connection"] = 'local'
                except Exception, ex:
                    logger.warn(msg="id:{assets}, error:{ex}".format(assets=assets.id, ex=ex))
            # if assets.host_vars:
            #     try:
            #         for k, v in eval(assets.host_vars).items():
            #             if k not in ["ip", "port", "username", "password", "ip"]: data[k] = v
            #     except Exception, ex:
            #         logger.warn(msg="资产: {assets},转换host_vars失败:{ex}".format(assets=assets.id, ex=ex))
            resource.append(data)
        return sList, resource

    def inventory(self, inventory):
        sList = []
        resource = {}
        groups = ''
        try:
            inventory = Ansible_Inventory.objects.get(id=inventory)
        except Exception, ex:
            logger.warn(msg="资产组查询失败：{id}".format(id=inventory, ex=ex))
        for ds in inventory.inventory_group.all():
            resource[ds.group_name] = {}
            hosts = []
            for ser in ds.inventory_group_server.all():
                assets = Assets.objects.get(id=ser.server)
                data = {}
                if hasattr(assets, 'server_asset'):
                    try:
                        serverIp = assets.server_asset.ip
                        data["ip"] = serverIp
                        if assets.server_asset.port: data["port"] = int(assets.server_asset.port)
                        data["username"] = assets.server_asset.username
                        data["sudo_passwd"] = assets.server_asset.sudo_passwd
                        data["password"] = assets.server_asset.passwd
                        # if assets.server_asset.keyfile != 1: data["password"] = assets.server_asset.passwd
                    except Exception, ex:
                        logger.warn(msg="id:{assets}, error:{ex}".format(assets=assets.id, ex=ex))
                elif hasattr(assets, 'network_asset'):
                    try:
                        serverIp = assets.network_asset.ip
                        data["ip"] = serverIp
                        if assets.server_asset.port: data["port"] = int(assets.network_asset.port)
                        data["password"] = assets.network_asset.passwd,
                        data["username"] = assets.network_asset.username
                        data["sudo_passwd"] = assets.network_asset.sudo_passwd
                        data["connection"] = 'local'
                    except Exception, ex:
                        logger.warn(msg="id:{assets}, error:{ex}".format(assets=assets.id, ex=ex))
                if assets.host_vars:
                    try:
                        for k, v in eval(assets.host_vars).items():
                            if k not in ["ip", "port", "username", "password", "ip"]: data[k] = v
                    except Exception, ex:
                        logger.warn(msg="资产: {assets},转换host_vars失败:{ex}".format(assets=assets.id, ex=ex))
                if serverIp not in sList: sList.append(serverIp)
                hosts.append(data)
            resource[ds.group_name]['hosts'] = hosts
            groups += ds.group_name + ','
            try:
                if ds.ext_vars: resource[ds.group_name]['vars'] = eval(ds.ext_vars)
            except Exception, ex:
                logger.warn(msg="资产组变量转换失败: {id} {ex}".format(id=inventory, ex=ex))
                resource[ds.group_name]['vars'] = None
        return sList, resource, groups