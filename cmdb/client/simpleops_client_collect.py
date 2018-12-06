#! /usr/bin/env python
# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import platform
import sys
import urllib
import urllib2

reload(sys)
sys.setdefaultencoding('utf8')

token = "uDRpMS8MoyCr6SZ5"
url = "http://127.0.0.1:8000/cmdb/report/"


def report_data(data):
    """
    创建测试用例
    :return:
    """
    # 将数据打包到一个字典内，并转换为json格式
    data = {"asset_data": json.dumps(data), "token": token}
    # 根据settings中的配置，构造url
    # url = "http://%s:%s%s" % (settings.Params['server'], settings.Params['port'], settings.Params['url'])
    print('正在将数据发送至： [%s]  ......' % url)
    try:
        # 使用Python内置的urllib.request库，发送post请求。
        # 需要先将数据进行封装，并转换成bytes类型
        # data_encode = urllib.parse.urlencode(data).encode()  #python3的使用方法
        data_encode = urllib.urlencode(data).encode()
        response = urllib2.urlopen(url=url, data=data_encode, timeout=10)
        # response = urllib.request.urlopen(url=url, data=data_encode, timeout=settings.Params['request_timeout']) #python3的使用方式

        print("\033[31;1m发送完毕！\033[0m ")
        message = response.read()
        print("返回结果：%s" % message)
    except Exception as e:
        message = "发送失败"
        print("\033[31;1m发送失败，%s\033[0m" % e)


class Linux_sys_info_collect():
    def __init__(self):
        pass

    @classmethod
    def collect(cls):
        filter_keys = ['Manufacturer', 'Serial Number', 'Product Name', 'UUID', 'Wake-up Type']
        raw_data = {}

        for key in filter_keys:
            try:
                res = subprocess.Popen("sudo dmidecode -t system|grep '%s'" % key,
                                       stdout=subprocess.PIPE, shell=True)
                result = res.stdout.read().decode()
                data_list = result.split(':')

                if len(data_list) > 1:
                    raw_data[key] = data_list[1].strip()
                else:
                    raw_data[key] = -1
            except Exception as e:
                print(e)
                raw_data[key] = -2

        data = dict()
        data['asset_type'] = 'server'
        data['manufacturer'] = raw_data['Manufacturer']
        data['sn'] = raw_data['Serial Number']
        data['model'] = raw_data['Product Name']
        data['uuid'] = raw_data['UUID']
        data['wake_up_type'] = raw_data['Wake-up Type']

        data.update(cls.get_os_info())
        data.update(cls.get_cpu_info())
        data.update(cls.get_ram_info())
        data.update(cls.get_nic_info())
        data.update(cls.get_disk_info())
        return data

    @classmethod
    def get_os_info(cls):
        """
        获取操作系统信息
        :return:
        """
        distributor = subprocess.Popen("lsb_release -a|grep 'Distributor ID'",
                                       stdout=subprocess.PIPE, shell=True)
        distributor = distributor.stdout.read().decode().split(":")

        release = subprocess.Popen("lsb_release -a|grep 'Description'",
                                   stdout=subprocess.PIPE, shell=True)

        release = release.stdout.read().decode().split(":")
        data_dic = {
            "os_distribution": distributor[1].strip() if len(distributor) > 1 else "",
            "os_release": release[1].strip() if len(release) > 1 else "",
            "os_type": "Linux",
        }
        return data_dic

    @classmethod
    def get_cpu_info(cls):
        """
        获取cpu信息
        :return:
        """
        base_cmd = 'cat /proc/cpuinfo'

        raw_data = {
            'cpu_model': "%s |grep 'model name' |head -1 " % base_cmd,
            'cpu_count': "%s |grep  'processor'|wc -l " % base_cmd,
            'cpu_core_count': "%s |grep 'cpu cores' |awk -F: '{SUM +=$2} END {print SUM}'" % base_cmd,
        }

        for key, cmd in raw_data.items():
            try:
                cmd_res = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                raw_data[key] = cmd_res.stdout.read().decode().strip()
            except ValueError as e:
                print(e)
                raw_data[key] = ""

        data = {
            "cpu_count": raw_data["cpu_count"],
            "cpu_core_count": raw_data["cpu_core_count"]
        }

        cpu_model = raw_data["cpu_model"].split(":")

        if len(cpu_model) > 1:
            data["cpu_model"] = cpu_model[1].strip()
        else:
            data["cpu_model"] = -1

        return data

    @classmethod
    def get_ram_info(cls):
        """
        获取内存信息
        :return:
        """
        raw_data = subprocess.Popen("sudo dmidecode -t memory", stdout=subprocess.PIPE, shell=True)
        raw_list = raw_data.stdout.read().decode().split("\n")
        raw_ram_list = []
        item_list = []
        for line in raw_list:
            if line.startswith("Memory Device"):
                raw_ram_list.append(item_list)
                item_list = []
            else:
                item_list.append(line.strip())

        ram_list = []
        for item in raw_ram_list:
            item_ram_size = 0
            ram_item_to_dic = {}
            for i in item:
                data = i.split(":")
                if len(data) == 2:
                    key, v = data
                    if key == 'Size':
                        if v.strip() != "No Module Installed":
                            ram_item_to_dic['capacity'] = v.split()[0].strip()
                            item_ram_size = round(float(v.split()[0]))
                        else:
                            ram_item_to_dic['capacity'] = 0

                    if key == 'Type':
                        ram_item_to_dic['model'] = v.strip()
                    if key == 'Manufacturer':
                        ram_item_to_dic['manufacturer'] = v.strip()
                    if key == 'Serial Number':
                        ram_item_to_dic['sn'] = v.strip()
                    if key == 'Asset Tag':
                        ram_item_to_dic['asset_tag'] = v.strip()
                    if key == 'Locator':
                        ram_item_to_dic['slot'] = v.strip()

            if item_ram_size == 0:
                pass
            else:
                ram_list.append(ram_item_to_dic)

        raw_total_size = subprocess.Popen("cat /proc/meminfo|grep MemTotal ", stdout=subprocess.PIPE, shell=True)
        raw_total_size = raw_total_size.stdout.read().decode().split(":")
        ram_data = {'ram': ram_list}
        if len(raw_total_size) == 2:
            total_gb_size = int(raw_total_size[1].split()[0]) / 1024 ** 2
            ram_data['ram_size'] = total_gb_size

        return ram_data

    @classmethod
    def get_nic_info(cls):
        """
        获取网卡信息
        :return:
        """
        raw_data = subprocess.Popen("ifconfig -a", stdout=subprocess.PIPE, shell=True)

        raw_data = raw_data.stdout.read().decode().split("\n")

        nic_dic = dict()
        next_ip_line = False
        last_mac_addr = None

        for line in raw_data:
            if next_ip_line:
                next_ip_line = False
                nic_name = last_mac_addr.split()[0]
                mac_addr = last_mac_addr.split("HWaddr")[1].strip()
                raw_ip_addr = line.split("inet addr:")
                raw_bcast = line.split("Bcast:")
                raw_netmask = line.split("Mask:")
                if len(raw_ip_addr) > 1:
                    ip_addr = raw_ip_addr[1].split()[0]
                    network = raw_bcast[1].split()[0]
                    netmask = raw_netmask[1].split()[0]
                else:
                    ip_addr = None
                    network = None
                    netmask = None
                if mac_addr not in nic_dic:
                    nic_dic[mac_addr] = {'name': nic_name,
                                         'mac': mac_addr,
                                         'net_mask': netmask,
                                         'network': network,
                                         'bonding': 0,
                                         'model': 'unknown',
                                         'ip_address': ip_addr,
                                         }
                else:
                    if '%s_bonding_addr' % (mac_addr,) not in nic_dic:
                        random_mac_addr = '%s_bonding_addr' % (mac_addr,)
                    else:
                        random_mac_addr = '%s_bonding_addr2' % (mac_addr,)

                    nic_dic[random_mac_addr] = {'name': nic_name,
                                                'mac': random_mac_addr,
                                                'net_mask': netmask,
                                                'network': network,
                                                'bonding': 1,
                                                'model': 'unknown',
                                                'ip_address': ip_addr,
                                                }

            if "HWaddr" in line:
                next_ip_line = True
                last_mac_addr = line
        nic_list = []
        for k, v in nic_dic.items():
            nic_list.append(v)

        return {'nic': nic_list}

    @classmethod
    def get_disk_info(cls):
        """
        获取存储信息。
        本脚本只针对ubuntu中使用sda，且只有一块硬盘的情况。
        具体查看硬盘信息的命令，请根据实际情况，实际调整。
        如果需要查看Raid信息，可以尝试MegaCli工具。
        :return:
        """
        raw_data = subprocess.Popen("sudo hdparm -i /dev/sda | grep Model", stdout=subprocess.PIPE, shell=True)
        raw_data = raw_data.stdout.read().decode()
        data_list = raw_data.split(",")
        model = data_list[0].split("=")[1]
        sn = data_list[2].split("=")[1].strip()

        size_data = subprocess.Popen("sudo fdisk -l /dev/sda | grep Disk|head -1", stdout=subprocess.PIPE, shell=True)
        size_data = size_data.stdout.read().decode()
        size = size_data.split(":")[1].strip().split(" ")[0]

        result = {'physical_disk_driver': []}
        disk_dict = dict()
        disk_dict["model"] = model
        disk_dict["size"] = size
        disk_dict["sn"] = sn
        result['physical_disk_driver'].append(disk_dict)

        return result


class Windows_sys_info_collect():

    @staticmethod
    def collect():
        data = {
            'os_type': platform.system(),
            'os_release': "%s %s  %s " % (platform.release(), platform.architecture()[0], platform.version()),
            'os_distribution': 'Microsoft',
            'asset_type': 'server'
        }

        # 分别获取各种硬件信息
        win32obj = Win32Info()
        data.update(win32obj.get_cpu_info())
        data.update(win32obj.get_ram_info())
        data.update(win32obj.get_motherboard_info())
        data.update(win32obj.get_disk_info())
        data.update(win32obj.get_nic_info())
        # 最后返回一个数据字典
        return data


class Win32Info(object):

    def __init__(self):
        # 固定用法，更多内容请参考模块说明
        self.wmi_obj = wmi.WMI()
        self.wmi_service_obj = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        self.wmi_service_connector = self.wmi_service_obj.ConnectServer(".", "root\cimv2")

    def get_cpu_info(self):
        """
        获取CPU的相关数据，这里只采集了三个数据，实际有更多，请自行选择需要的数据
        :return:
        """
        data = {}
        cpu_lists = self.wmi_obj.Win32_Processor()
        cpu_core_count = 0
        for cpu in cpu_lists:
            cpu_core_count += cpu.NumberOfCores

        cpu_model = cpu_lists[0].Name  # CPU型号（所有的CPU型号都是一样的）
        data["cpu_number"] = len(cpu_lists)  # CPU个数
        data["cpu_model"] = cpu_model
        data["cpu_core"] = cpu_core_count  # CPU总的核数

        return data

    def get_ram_info(self):
        """
        收集内存信息
        :return:
        """
        data = []
        # 这个模块用SQL语言获取数据
        ram_collections = self.wmi_service_connector.ExecQuery("Select * from Win32_PhysicalMemory")
        for item in ram_collections:  # 主机中存在很多根内存，要循环所有的内存数据
            ram_size = int(int(item.Capacity) / (1024 ** 3))  # 转换内存单位为GB
            item_data = {
                "slot": item.DeviceLocator.strip(),
                "capacity": ram_size,
                "model": item.Caption,
                "manufacturer": item.Manufacturer,
                "sn": item.SerialNumber,
            }
            data.append(item_data)  # 将每条内存的信息，添加到一个列表里

        return {"ram": data}  # 再对data列表封装一层，返回一个字典，方便上级方法的调用

    def get_motherboard_info(self):
        """
        获取主板信息
        :return:
        """
        computer_info = self.wmi_obj.Win32_ComputerSystem()[0]
        system_info = self.wmi_obj.Win32_OperatingSystem()[0]
        data = dict()
        data['manufacturer'] = computer_info.Manufacturer
        data['model'] = computer_info.Model
        data['wake_up_type'] = computer_info.WakeUpType
        data['sn'] = system_info.SerialNumber
        return data

    def get_disk_info(self):
        """
        硬盘信息
        :return:
        """
        data = []
        for disk in self.wmi_obj.Win32_DiskDrive():  # 每块硬盘都要获取相应信息
            item_data = dict()
            iface_choices = ["SAS", "SCSI", "SATA", "SSD"]
            for iface in iface_choices:
                if iface in disk.Model:
                    item_data['iface_type'] = iface
                    break
            else:
                item_data['iface_type'] = 'unknown'
            item_data['slot'] = disk.Index
            item_data['sn'] = disk.SerialNumber
            item_data['model'] = disk.Model
            item_data['manufacturer'] = disk.Manufacturer
            item_data['capacity'] = int(int(disk.Size) / (1024 ** 3))
            data.append(item_data)

        return {'physical_disk_driver': data}

    def get_nic_info(self):
        """
        网卡信息
        :return:
        """
        data = []
        for nic in self.wmi_obj.Win32_NetworkAdapterConfiguration():
            if nic.MACAddress is not None:
                item_data = dict()
                item_data['mac'] = nic.MACAddress
                item_data['model'] = nic.Caption
                item_data['name'] = nic.Index
                if nic.IPAddress is not None:
                    item_data['ip_address'] = nic.IPAddress[0]
                    item_data['net_mask'] = nic.IPSubnet
                else:
                    item_data['ip_address'] = ''
                    item_data['net_mask'] = ''
                data.append(item_data)

        return {'nic': data}


if __name__ == '__main__':
    osname = platform.system()
    if osname == "Linux":
        import subprocess

        linux_data = Linux_sys_info_collect.collect()
        report_data(linux_data)
    elif osname == "Windows":
        import win32com
        import wmi

        win_data = Windows_sys_info_collect.collect()
        report_data(win_data)
    else:
        sys.exit("不支持当前操作系统： [%s]! " % platform.system())
