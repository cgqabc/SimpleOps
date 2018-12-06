#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from django.core.mail import send_mail
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.getdefaultencoding()

os.environ['DJANGO_SETTINGS_MODULE'] = 'SimpleOps.settings'

if __name__ == '__main__':

    send_mail('django测试资料','这是一封测试邮件，给自己的。加油，django内容随后发送！','ken178453063@163.com',
              ['alancao@live.cn',])
