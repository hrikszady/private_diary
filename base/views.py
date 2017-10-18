# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.views.generic import TemplateView
from base.decorator import (get_method as get, post_method as post)
from base.forms import (LoginForm, SignUPForm, ProfileForm)
from base.models import User
# from methods import *


class HomePageView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', None)


@get
def login(request, methods="GET"):
    form = LoginForm()
    return render(request, 'login.html', {'form': form})


@get
def signup(request, methods="GET"):
    form = SignUPForm()
    signup = True
    return render(request, 'signup.html', {
        'form': form, 'signup': signup
    })


@get
@csrf_exempt
def profile(request, methods="GET"):
    user_id = request.GET.get('id', '')
    user = User.objects.get(id=user_id)
    form = ProfileForm()
    form.fields['alternate_phone_no'].initial = user.alternate_phone_no
    form.fields['std_code'].initial = user.std_code
    form.fields['alternate_email'].initial = user.alternate_email
    form.fields['pincode'].initial = user.pincode
    form.fields['address'].initial = user.address
    form.fields['hobbies'].initial = user.hobbies
    profile = True
    return render(request, 'signup.html', {
        'form': form, 'profile': profile,
    })


@post
@csrf_exempt
def signupsubmit(request, data):
    form = LoginForm()

    return render(request, 'signup.html', {
        'form': form, 'signup': signup
    })
