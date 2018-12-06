#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http

# @channel_session_user_from_http
# def ws_connect(message):
#     Group('users').add(message.reply_channel)
#     Group('users').send({
#         'text': json.dumps({
#             'username': message.user.username,
#             'is_logged_in': True
#         })
#     })
#
# @channel_session_user
# def ws_disconnect(message):
#     Group('users').send({
#         'text': json.dumps({
#             'username': message.user.username,
#             'is_logged_in': False
#         })
#     })
#     Group('users').discard(message.reply_channel)

from channels.generic.websockets import WebsocketConsumer
class UserConsumer(WebsocketConsumer):
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
        return ["users"]
    def connect(self, message, **kwargs):
        """
        Perform things on connection start
        """
        # Accept the connection; this is done by default if you don't override
        # the connect function.
        # self.message.reply_channel.send({"accept": True})
        # print self.message.user.username
        Group('users').send({
            'text': json.dumps({
                'username': self.message.user.username,
                'is_logged_in': True,
                # 'online_user_num': OnlineUser.objects.count()
            })
        })
    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        Group('users').send({
            'text': json.dumps({
                'username': self.message.user.username,
                'is_logged_in': False,
                # 'online_user_num': OnlineUser.objects.count()
            })
        })
        Group('users').discard(self.message.reply_channel)