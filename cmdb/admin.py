# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models, asset_handler


# Register your models here.
class Asset_admin(admin.ModelAdmin):
    list_display = ['asset_type', 'name', 'status', 'c_time', 'm_time']

class Public_admin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(Public_admin, self).__init__(model, admin_site)


class NewAsset_admin(admin.ModelAdmin):
    list_display = ['asset_type', 'sn', 'model', 'manufacturer', 'c_time', 'm_time']
    list_filter = ['asset_type', 'manufacturer', 'c_time']
    search_fields = ('sn',)

    actions = ['approve_selected_new_assets']

    def approve_selected_new_assets(self, request, queryset):
        # 获得被打钩的checkbox对应的资产
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        success_upline_number = 0
        for asset_id in selected:
            obj = asset_handler.ApproveAsset(request, asset_id)
            ret = obj.asset_upline()
            if ret:
                success_upline_number += 1
        # 顶部绿色提示信息
        self.message_user(request, "成功批准  %s  条新资产上线！" % success_upline_number)

    approve_selected_new_assets.short_description = "批准选择的新资产"


admin.site.register(models.Assets, Asset_admin)
admin.site.register(models.NewAssetApprovalZone, NewAsset_admin)
admin.site.register(models.BusinessUnit,Public_admin)
admin.site.register(models.Contract,Public_admin)
admin.site.register(models.Disk_asset,Public_admin)
admin.site.register(models.EventLog,Public_admin)
admin.site.register(models.IDC,Public_admin)
admin.site.register(models.Manufacturer,Public_admin)
admin.site.register(models.Middleware,Public_admin)
admin.site.register(models.NIC,Public_admin)
admin.site.register(models.Ram_asset,Public_admin)
admin.site.register(models.SecurityDevice,Public_admin)
admin.site.register(models.Network_asset,Public_admin)
admin.site.register(models.Service_Assets,Public_admin)
admin.site.register(models.Server_asset,Public_admin)
admin.site.register(models.Tag,Public_admin)
