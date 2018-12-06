#! /usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib

from django.contrib import auth
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponseRedirect

import forms
from models import User_info


# Create your views here.
def hash_code(code, salt='mysalt'):
    h = hashlib.sha256()
    code += salt
    h.update(code.encode())  # update方法只接受bytes类型
    return h.hexdigest()


def login(request):
    # if request.session.get('is_login',None):
    #     return redirect('/index/')
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        login_form = forms.User_form(request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['passwd']
            user = auth.authenticate(request, username=username, password=password)
            # 设置用户的会话过期时间,如果没有勾记住我，默认关闭浏览器就要重新登录
            if not request.POST.get('remember_me', None):
                request.session.set_expiry(0)
            if user is not None:
                if user.is_active:
                    # user = User_info.objects.get(name=username)
                    # userpass = hash_code(userpass)
                    # if userpass == user.passwd:
                    #     request.session['is_login'] = True
                    #     request.session['user_id'] = user.id
                    #     request.session['user_name'] = user.name
                    #     return redirect('/index/')
                    # else:
                    #     message = "密码错误"
                    auth.login(request, user)
                    request.session['is_login'] = True
                    request.session['username'] = username
                    # return HttpResponseRedirect(request.POST['next'])
                    return HttpResponseRedirect('/index/')

                else:
                    # print(e)
                    message = "用户未激活！"
                    # print login_form
                    return render(request, 'accounts/login.html', locals())
        else:
            message = "用户名或密码错误！"
    login_form = forms.User_form()
    return render(request, 'accounts/login.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    request.session.flush()
    return redirect('/login/')


def register(request):
    if request.method == "POST":
        register_form = forms.Register_form(request.POST)
        # messages.success(request, '注册成功')
        # message = '请检查填写内容！'
        if register_form.is_valid():
            user = User_info()
            username = register_form.cleaned_data['name']
            passwd = register_form.cleaned_data['passwd']
            passwd2 = register_form.cleaned_data['passwd2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if not passwd == passwd2:
                message = '两次密码输入不一致！'
                return render(request, 'accounts/register.html', locals())
            else:
                user_same = User_info.objects.filter(name=username)
                if username == user_same:
                    message = "用户名已存在！！"
                    return render(request, 'accounts/register.html', locals())
                email_same = User_info.objects.filter(email=email)
                if email == email_same:
                    message = "该邮箱已被注册，请更换邮箱！！"
                    return render(request, 'accounts/register.html', locals())
            passwd = hash_code(passwd)
            # user.objects.create(username,passwd,email,sex)
            user.username = username
            user.password = passwd
            user.email = email
            user.sex = sex
            user.save()
            messages.success(request, '注册成功')
            return redirect('/login/')
        else:
            message = register_form.errors

    register_form = forms.Register_form()
    return render(request, 'accounts/register.html', locals())
