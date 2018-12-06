#! /usr/bin/env python
# -*- coding: utf-8 -*-
# from channels.routing import route
from chat.consumers import ChatConsumer #导入处理函数
from accounts.consumers import UserConsumer


channel_routing = [
    ChatConsumer.as_route(path=r"/chat/",attrs={'group': 'chat', 'group_prefix': 'pre'}),
    UserConsumer.as_route(path=r"/user/", attrs={'group': 'users', 'group_prefix': 'pre'}),
]
