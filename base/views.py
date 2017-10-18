# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.views.generic import TemplateView
from base.forms import LoginForm, SignUPForm
from base.decorator import get_method as get
# from methods import *


class HomePageView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', None)


@get
@csrf_exempt
def login(request, methods="GET"):
    form = LoginForm()
    return render(request, 'login.html', {'form': form})


@get
@csrf_exempt
def signup(request, methods="GET"):
    form = SignUPForm()
    signup = True
    return render(request, 'signup.html', {
        'form': form, 'signup': signup
    })
