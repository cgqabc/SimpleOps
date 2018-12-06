# -*- coding: utf-8 -*-
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
# from .authentication.models import OnlineUser
import json
from datetime import datetime

# message.reply_channel    一个客户端通道的对象
# message.reply_channel.send(chunk)  用来唯一返回这个客户端
#
# 一个管道大概会持续30s


# 当连接上时，发回去一个connect字符串
@channel_session_user_from_http
def ws_connect(message):
    print('connect')
    print(datetime.now())
    room = message.content['path'].strip("/")
    print(room)
    # message.reply_channel.send({'accept': True})

    Group('users').add(message.reply_channel)
    Group('users').send({
        'text': json.dumps({
            'username': message.user.username,
            'is_logged_in': True,
            # 'online_user_num': OnlineUser.objects.count()
        })
    })


# 将发来的信息原样返回
@channel_session_user
def ws_receive(message):
    print('message',)
    print(message.channel)
    print(datetime.now())
    # message.reply_channel.send({
    #     "text": message.content['text'],
    # })
    Group('users').send({
        'text': json.dumps({
            # 'message': True,
            # "text": message.content['text'],
            "message": json.loads(message.content['text'])["message"],
        })
    })


# 断开连接时发送一个disconnect字符串，当然，他已经收不到了
@channel_session_user
def ws_disconnect(message):
    print('disconnect')
    print(datetime.now())

    Group('users').send({
        'text': json.dumps({
            'username': message.user.username,
            'is_logged_in': False,
            # 'online_user_num': OnlineUser.objects.count()
        })
    })
    Group('users').discard(message.reply_channel)
    # message.reply_channel.send({'accept': True})




##############类视图的方式########################
from channels.generic.websockets import WebsocketConsumer
class ChatConsumer(WebsocketConsumer):
    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    http_user = True
    # Set to True if you want it, else leave it out
    strict_ordering = False
    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        return ["chat"]
    def connect(self, message, **kwargs):
        """
        Perform things on connection start
        """
        # Accept the connection; this is done by default if you don't override
        # the connect function.
        # self.message.reply_channel.send({"accept": True})
        # print self.message.user.username
        Group('chat').send({
            'text': json.dumps({
                'username': self.message.user.username,
                'is_logged_in': True,
                # 'online_user_num': OnlineUser.objects.count()
            })
        })
    def receive(self, text=None, bytes=None, **kwargs):
        """
        Called when a message is received with either text or bytes
        filled out.
        """
        # Simple echo
        # self.send(text=text, bytes=bytes)
        # print text
        Group('chat').send({
            'text': json.dumps({
                # 'message': True,
                # "text": message.content['text'],
                "message": json.loads(text)["message"],
            })
        })
    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        Group('chat').send({
            'text': json.dumps({
                'username': self.message.user.username,
                'is_logged_in': False,
                # 'online_user_num': OnlineUser.objects.count()
            })
        })
        Group('chat').discard(self.message.reply_channel)