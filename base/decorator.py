# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from base.methods import (
    create_guest, get_ip_address, FormData,
    verify_user_session
)
from django.shortcuts import render, redirect

def get_method(f, methods={"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0}):
    def wrap(request, *args, **kwargs):
        if request.method != 'GET':
            return bad_request(request)
        return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def post_method(f, methods={"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0}):
    def wrap(request, *args, **kwargs):
        if request.method != 'POST':
            return bad_request(request)
        data = FormData(request)
        request.POST = {}
        return f(request, data, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def bad_request(request):
    response = {
        "errorCode": "403",
        "message": "Bad Request"
    }
    return JsonResponse(response, status=403)


def guest(f, methods={"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0}):
    def wrap(request, *args, **kwargs):
        ip_address = get_ip_address(request)
        guest_id = request.request.session.get('guest_id', None)
        user_session, user = verify_user_session(request)
        if guest_id is None and user_session:
            request.request.session['guest_id'] = create_guest(ip_address)
            return redirect('/account/user/signin')
        return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap

def auth_user(f, methods={"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0}):
    def wrap(request, *args, **kwargs):
        if request.method != 'GET':
            return bad_request(request)
        return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap

