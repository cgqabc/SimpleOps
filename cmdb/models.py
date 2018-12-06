# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from accounts.models import User_info


# Create your models here.
class Assets(models.Model):
    asset_type_choice = (
        ('server', '物理机'),
        ('vmserver', '虚拟机'),
        ('docker', '容器'),
        ('netdevice', '网络设备'),
        ('storagedevice', '存储设备'),
        ('others', '其他'),
    )
    asset_status_choice = (
        ('1', '在线'),
        ('2', '下线'),
        ('3', '故障'),
        ('4', '备用'),
        ('5', '未知'),
    )
    asset_type = models.CharField(choices=asset_type_choice, max_length=60, default='vmserver', verbose_name='资产类型')
    name = models.CharField(max_length=100, verbose_name='资产名称', unique=True)
    sn = models.CharField(max_length=100, verbose_name='资产序号', unique=True)
    status = models.CharField(choices=asset_status_choice, max_length=10, default='1', verbose_name='资产状态')
    business_unit = models.ForeignKey('BusinessUnit', null=True, blank=True,
                                      related_name='project_assets',verbose_name='所属业务线')

    service = models.SmallIntegerField(blank=True, null=True, verbose_name='所属业务')
    group = models.SmallIntegerField(blank=True, null=True, verbose_name='分组')
    asset_model = models.CharField(max_length=100, blank=True, null=True, verbose_name='资产型号')
    manufacturer = models.ForeignKey('Manufacturer', blank=True, null=True,
                                     related_name='manufacturer_assets',verbose_name='供货商')
    site = models.CharField(blank=True, null=True, max_length=100, verbose_name='位置')
    manage_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='管理IP')
    manager = models.CharField(blank=True, null=True, max_length=100, verbose_name='管理人员')

    buy_time = models.DateField(blank=True, null=True, verbose_name='购买时间')
    expire_date = models.DateField(null=True, blank=True, verbose_name='过保时间')
    approved_by = models.ForeignKey(User_info, verbose_name='批准人', null=True, blank=True, related_name='approved_by')
    memo = models.TextField(null=True, blank=True, verbose_name='备注')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')

    def __unicode__(self):
        return "{0}|{1}".format(self.name,self.manage_ip)

    class Meta:
        verbose_name = '总资产表'
        verbose_name_plural = '总资产表'
        ordering = ['-c_time']


class Server_asset(models.Model):
    created_by_choice = (
        ('auto', '自动添加'),
        ('manual', '手工录入'),
    )
    asset = models.OneToOneField('Assets')
    created_by = models.CharField(choices=created_by_choice, max_length=32, default='auto', verbose_name="添加方式")
    hosted_on = models.ForeignKey('self', related_name='hosted_on_server',
                                  blank=True, null=True, verbose_name="宿主机")
    model = models.CharField(max_length=128, null=True, blank=True, verbose_name='服务器型号')
    raid_type = models.CharField(max_length=512, blank=True, null=True, verbose_name='Raid类型')

    ip = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name="IP")
    hostname = models.CharField(max_length=100, blank=True, null=True, verbose_name="主机名")
    username = models.CharField(max_length=100, blank=True, null=True, verbose_name="用户名")
    passwd = models.CharField(max_length=100, blank=True, null=True, verbose_name="密码")
    sudo_passwd = models.CharField(max_length=100, blank=True, null=True, verbose_name="sudo密码")
    keyfile = models.CharField(max_length=100, blank=True, null=True,
                               verbose_name="密钥路径")  # FileField(upload_to = './upload/key/',blank=True,null=True,verbose_name='密钥文件')
    port = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True, verbose_name="端口")
    line = models.CharField(max_length=100, blank=True, null=True, verbose_name='线路')
    # cpu_model = models.CharField(max_length=100, blank=True, null=True, verbose_name='cpu型号')
    # cpu_number = models.SmallIntegerField(blank=True, null=True, verbose_name='cpu个数')
    # cpu_core = models.SmallIntegerField(blank=True, null=True, verbose_name='cpu核数')
    disk_total = models.CharField(max_length=100, blank=True, null=True, verbose_name='磁盘容量')
    ram_total = models.CharField(max_length=100, blank=True, null=True, verbose_name='内存容量')
    swap = models.CharField(max_length=100, blank=True, null=True, verbose_name='swap')
    raid = models.SmallIntegerField(blank=True, null=True, verbose_name='raid方式')

    os_type = models.CharField(max_length=64, blank=True, null=True, verbose_name="操作系统类型")
    os_distribution = models.CharField(verbose_name='发行版本', max_length=64, blank=True, null=True)
    os_release = models.CharField(verbose_name='操作系统版本', max_length=64, blank=True, null=True)

    def __unicode__(self):
        # return '%s--%s <sn:%s>' % (self.asset.name, self.asset.asset_model, self.asset.sn)
        # return self.asset.name
        return "{0}|{1}".format(self.asset.name, self.asset.manage_ip)
    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = "服务器"


class Network_asset(models.Model):
    assets = models.OneToOneField('Assets')
    bandwidth = models.CharField(max_length=100, blank=True, null=True, verbose_name='背板带宽')
    ip = models.CharField(unique=True, max_length=100, blank=True, null=True, verbose_name='管理ip')
    username = models.CharField(max_length=100, blank=True, null=True)
    passwd = models.CharField(max_length=100, blank=True, null=True)
    sudo_passwd = models.CharField(max_length=100, blank=True, null=True)
    port = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    port_number = models.SmallIntegerField(blank=True, null=True, verbose_name='端口个数')
    firmware = models.CharField(max_length=100, blank=True, null=True, verbose_name='固件版本')
    cpu = models.CharField(max_length=100, blank=True, null=True, verbose_name='cpu型号')
    stone = models.CharField(max_length=100, blank=True, null=True, verbose_name='内存大小')
    configure_detail = models.TextField(max_length=100, blank=True, null=True, verbose_name='配置说明')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.assets.name

    class Meta:
        verbose_name = '网络资产表'
        verbose_name_plural = '网络资产表'


class NIC(models.Model):
    """网卡组件"""

    asset = models.ForeignKey('Assets')  # 注意要用外键
    name = models.CharField('网卡名称', max_length=64, blank=True, null=True)
    model = models.CharField('网卡型号', max_length=128)
    mac = models.CharField('MAC地址', max_length=64)  # 虚拟机有可能会出现同样的mac地址
    ip_address = models.GenericIPAddressField('IP地址', blank=True, null=True)
    net_mask = models.CharField('掩码', max_length=64, blank=True, null=True)
    bonding = models.CharField('绑定地址', max_length=64, blank=True, null=True)
    active = models.BooleanField('是否在线', default=True)

    def __unicode__(self):
        return '%s:  %s:  %s' % (self.asset.name, self.model, self.mac)

    class Meta:
        verbose_name = '网卡'
        verbose_name_plural = "网卡"
        unique_together = ('asset', 'model', 'mac')


class CPU(models.Model):
    """CPU组件"""

    asset = models.OneToOneField('Assets')
    cpu_model = models.CharField('CPU型号', max_length=128, blank=True, null=True)
    cpu_number = models.PositiveSmallIntegerField('物理CPU个数', default=1)
    cpu_core = models.PositiveSmallIntegerField('CPU核数', default=1)

    def __unicode__(self):
        # return self.asset.name + ":   " + self.cpu_model
        return self.asset.name
    class Meta:
        verbose_name = 'CPU'
        verbose_name_plural = "CPU"

class Ram_asset(models.Model):
    """内存组件"""

    asset = models.ForeignKey('Assets')  # 只能通过外键关联Asset。否则不能同时关联服务器、网络设备等等。
    sn = models.CharField('SN号', max_length=128, blank=True, null=True)
    model = models.CharField('内存型号', max_length=128, blank=True, null=True)
    manufacturer = models.CharField('内存制造商', max_length=128, blank=True, null=True)
    slot = models.CharField('插槽', max_length=64)
    capacity = models.IntegerField('内存大小(GB)', blank=True, null=True)
    device_status = models.CharField('内存状态', max_length=100, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.asset.name

    class Meta:
        verbose_name = '内存'
        verbose_name_plural = "内存"
        unique_together = ('asset', 'slot')  # 同一资产下的内存，根据插槽的不同，必须唯一


class Disk_asset(models.Model):
    """存储设备"""

    disk_interface_type_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
        ('unknown', 'unknown'),
    )

    asset = models.ForeignKey('Assets')
    sn = models.CharField('硬盘SN号', max_length=128)
    slot = models.CharField('所在插槽位', max_length=64, blank=True, null=True)
    model = models.CharField('磁盘型号', max_length=128, blank=True, null=True)
    manufacturer = models.CharField('磁盘制造商', max_length=128, blank=True, null=True)
    capacity = models.FloatField('磁盘容量(GB)', blank=True, null=True)
    interface_type = models.CharField('接口类型', max_length=16, choices=disk_interface_type_choice, default='unknown')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.asset.name

    class Meta:
        verbose_name = '硬盘'
        verbose_name_plural = "硬盘"
        unique_together = ('asset', 'sn')


class SecurityDevice(models.Model):
    """安全设备"""
    sub_asset_type_choice = (
        (0, '防火墙'),
        (1, '入侵检测设备'),
        (2, '互联网网关'),
        (4, '运维审计系统'),
    )

    asset = models.OneToOneField('Assets')
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="安全设备类型")

    def __unicode__(self):
        # return self.asset.name + "--" + self.get_sub_asset_type_display() + " id:%s" % self.id
        return self.asset.name
    class Meta:
        verbose_name = '安全设备'
        verbose_name_plural = "安全设备"


class IDC(models.Model):
    """机房"""
    name = models.CharField(max_length=64, unique=True, verbose_name="机房名称")
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = "机房"


class Manufacturer(models.Model):
    """厂商"""

    name = models.CharField('厂商名称', max_length=64, unique=True)
    telephone = models.CharField('支持电话', max_length=30, blank=True, null=True)
    memo = models.CharField('备注', max_length=128, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = "厂商"


class BusinessUnit(models.Model):
    """业务线"""

    parent_unit = models.ForeignKey('self', blank=True, null=True,
                                    related_name='parent_level',verbose_name="上级业务线")
    name = models.CharField('业务线', max_length=64, unique=True)
    memo = models.CharField('说明', max_length=64, blank=True, null=True)
    manager = models.CharField('负责人', max_length=64, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = "业务线"


class Service_Assets(models.Model):
    '''业务分组表'''
    business = models.ForeignKey('BusinessUnit', related_name='service_assets', on_delete=models.CASCADE,verbose_name="上级业务线")
    service_name = models.CharField(max_length=100,verbose_name="项目名称")
    memo = models.CharField('说明', max_length=64, blank=True, null=True)
    manager = models.CharField('负责人', max_length=64, blank=True, null=True)

    def __unicode__(self):
        return self.service_name

    class Meta:
        unique_together = (("business", "service_name"))
        verbose_name = '业务分组表'
        verbose_name_plural = '业务分组表'


class Middleware(models.Model):
    """    中间件软件    """
    name = models.CharField(max_length=100, verbose_name="中间件名称")
    version = models.CharField(max_length=64, help_text='例如: CentOS release 6.7 (Final)',
                               verbose_name='版本')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '中间件/软件'
        verbose_name_plural = "中间件/软件"
        unique_together = ('name', 'version')


class Contract(models.Model):
    """合同"""

    sn = models.CharField('合同号', max_length=128, unique=True)
    name = models.CharField('合同名称', max_length=64)
    memo = models.TextField('备注', blank=True, null=True)
    price = models.IntegerField('合同金额')
    detail = models.TextField('合同详细', blank=True, null=True)
    start_day = models.DateField('开始日期', blank=True, null=True)
    end_day = models.DateField('失效日期', blank=True, null=True)
    license_num = models.IntegerField('license数量', blank=True, null=True)
    c_day = models.DateField('创建日期', auto_now_add=True)
    m_day = models.DateField('修改日期', auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '合同'
        verbose_name_plural = "合同"


class Tag(models.Model):
    """标签"""
    name = models.CharField('标签名', max_length=32, unique=True)
    c_day = models.DateField('创建日期', auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = "标签"


class EventLog(models.Model):
    """
    日志.
    在关联对象被删除的时候，不能一并删除，需保留日志。
    因此，on_delete=models.SET_NULL
    """
    event_type_choice = (
        (0, '其它'),
        (1, '硬件变更'),
        (2, '新增配件'),
        (3, '设备下线'),
        (4, '设备上线'),
        (5, '定期维护'),
        (6, '业务上线\更新\变更'),
    )

    name = models.CharField('事件名称', max_length=128)
    asset = models.ForeignKey('Assets', blank=True, null=True, on_delete=models.SET_NULL)  # 当资产审批成功时有这项数据
    new_asset = models.ForeignKey('NewAssetApprovalZone', blank=True, null=True,
                                  on_delete=models.SET_NULL)  # 当资产审批失败时有这项数据
    event_type = models.SmallIntegerField('事件类型', choices=event_type_choice, default=4)
    component = models.CharField('事件子项', max_length=256, blank=True, null=True)
    detail = models.TextField('事件详情')
    date = models.DateTimeField('事件时间', auto_now_add=True)
    user = models.ForeignKey('User_info', blank=True, null=True, verbose_name='事件执行人',
                             on_delete=models.SET_NULL)  # 自动更新资产数据时没有执行人
    user = models.CharField('事件执行人', max_length=256, blank=True, null=True)
    memo = models.TextField('备注', blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '事件纪录'
        verbose_name_plural = "事件纪录"


class NewAssetApprovalZone(models.Model):
    """新资产待审批区"""

    asset_type_choice = (
        ('server', '物理机'),
        ('vmserver', '虚拟机'),
        ('docker', '容器'),
        ('netdevice', '网络设备'),
        ('storagedevice', '存储设备'),
        ('others', '其他'),
    )

    sn = models.CharField('资产SN号', max_length=128, unique=True)  # 此字段必填
    asset_type = models.CharField(choices=asset_type_choice, default='vmserver', max_length=64, blank=True, null=True,
                                  verbose_name='资产类型')
    manufacturer = models.CharField(max_length=64, blank=True, null=True, verbose_name='生产厂商')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='型号')
    # ram_size = models.PositiveIntegerField(blank=True, null=True, verbose_name='内存大小')
    ram_size = models.CharField(max_length=100, blank=True, null=True, verbose_name='内存大小')
    cpu_model = models.CharField(max_length=100, blank=True, null=True, verbose_name='cpu型号')
    cpu_number = models.SmallIntegerField(blank=True, null=True, verbose_name='cpu个数')
    cpu_core = models.SmallIntegerField(blank=True, null=True, verbose_name='cpu核数')

    os_type = models.CharField(max_length=64, blank=True, null=True, verbose_name="操作系统类型")
    os_distribution = models.CharField(verbose_name='发行版本', max_length=64, blank=True, null=True)
    os_release = models.CharField(verbose_name='操作系统版本', max_length=64, blank=True, null=True)

    data = models.TextField('资产数据')  # 此字段必填

    c_time = models.DateTimeField('汇报日期', auto_now_add=True)
    m_time = models.DateTimeField('数据更新日期', auto_now=True)
    approved = models.BooleanField('是否批准', default=False)

    def __unicode__(self):
        return self.sn

    class Meta:
        verbose_name = '新上线待批准资产'
        verbose_name_plural = "新上线待批准资产"
        ordering = ['-c_time']
