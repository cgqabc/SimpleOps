#! /usr/bin/env python
# -*- coding: utf-8 -*-
# import json
from django.http import HttpResponse,HttpResponseForbidden
from functools import wraps

def token_check(mytoken):
    def check(func):
        @wraps(func)
        def wapper(request,*args,**kwargs):
            if request.method == "POST":
                # token_info = request.POST.get("token")
                if mytoken == request.POST.get("token",default=None):
                    return func(request,*args,**kwargs)
                else:
                    return HttpResponse(status=403)
            elif request.method == "GET":
                # token_info =request.GET["token"]
                if mytoken == request.GET.get("token",default=None):
                    return func(request,*args,**kwargs)
                else:
                    # return HttpResponse("error!you don't hava permission", status=403)
                    return HttpResponse(status=403)
                    # return HttpResponseForbidden()
            return HttpResponse(status=403)
        return wapper
    return check