# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from base.methods import (
    create_guest, get_ip_address, FormData,
    verify_user_session, get_logged_session
)
from django.shortcuts import redirect


def get_method(
        f, methods={"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0}):
    def wrap(request, *args, **kwargs):
        if request.method != 'GET':
            return bad_request(request)
        return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def post_method(
        f, methods={"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0}):
    def wrap(request, *args, **kwargs):
        if request.method != 'POST':
            return bad_request(request)
        print 'here'
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


def guest(
        f, methods={"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0}):
    def wrap(request, *args, **kwargs):
        ip_address = get_ip_address(request)
        guest_id = request.request.session.get('guest_id', None)
        user_session = verify_user_session(request)
        if user_session:
            return redirect('/home')
        elif guest_id is None:
            request.request.session['guest_id'] = create_guest(ip_address)
        return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def is_authenticated(
        f, methods={"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0}):
    def wrap(request, *args, **kwargs):
        user_session, user = get_logged_session(request)
        if not user_session:
            return redirect('/')
        return f(request, user, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def is_unauthenticated(
        f, methods={"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0}):
    def wrap(request, *args, **kwargs):
        user_session = True \
            if 'user_token' in request.session.keys() else False
        if user_session:
            return redirect('/home')
        return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
