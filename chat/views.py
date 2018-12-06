# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Create your views here.

from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.utils.safestring import mark_safe
import json
from .models import Room
import logging
logger = logging.getLogger('django.chat')
def index(request):
    return render(request, 'chat/index.html', {})

# def room(request, room_name):
#     return render(request, 'chat/room.html', {
#         'room_name_json': mark_safe(json.dumps(room_name))
#     })

def room(request, room_name):
    # If the room with the given label doesn't exist, automatically create it
    # # upon first visit (a la etherpad).
    room, created = Room.objects.get_or_create(label=room_name)
    #
    # # We want to show the last 50 messages, ordered most-recent-last
    messages = reversed(room.messages.order_by('-timestamp')[:50])

    # print(room)
    return render(request, "chat/room.html", {
        'room': room_name,
        'messages': messages,
    })

def ajax(request):
    if request.method == 'GET':
        # logger.info('get!!!')
        # return render(request, 'chat/index.html', {"data":"i am get data"})
        return JsonResponse({"data":"i am get data"})
    elif request.method == 'POST':
        # print(request.POST)
        data = request.POST.get('ajdata')
        data = "i am post data: "+data
        # logger.info('post!!! %s' % data)
        # return render(request, 'chat/index.html', {"data": data})
        return JsonResponse({"data":data})