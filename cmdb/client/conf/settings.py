#! /usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

# 远端服务器配置
Params = {
    "server": "127.0.0.1",
    "port": 8000,
    'url': '/cmdb/report/',
    'request_timeout': 30,
}

# 日志文件配置

PATH = os.path.join(os.getcwd(), 'log', 'cmdb.log')


# 更多配置，请都集中在此文件中