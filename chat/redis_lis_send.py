#! /usr/bin/env python
# -*- coding: utf-8 -*-
import redis
import json
from channels import Group
# from django.core.management import BaseCommand
# 自定义命令，用于集成django环境，可以直接manage.py运行，但要放在commands/management/commands/目录下


##集成django环境####
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SimpleOps.settings")
django.setup()
##################
_redis = redis.Redis(host='127.0.0.1',port='6379')

def send_redis_data(msg):
    _redis.publish('chat', json.dumps(msg))


def getRedisData_for_send():
    pubsub = _redis.pubsub()
    pubsub.subscribe('chat')

    for i in pubsub.listen():
        print(i)
        if i['type'] == 'message':
            print(i['data'])
            Group('users').send(
                {'text':
                     json.dumps({'message':i['data']}),
                 })

send_redis_data({'name':'test',})  #由于订阅在后，所以这个发布没有作用。应该在其他地方等订阅后执行。
getRedisData_for_send()