#! /usr/bin/env python
# -*- coding: utf-8 -*-
from channels.routing import route
from .consumers import ws_connect, ws_disconnect

channel_routing = [
    route('websocket.connect', ws_connect),
    route('websocket.disconnect', ws_disconnect),
]