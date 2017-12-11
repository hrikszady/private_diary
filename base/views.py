# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from datetime import datetime
from base.decorator import (
    get_method as get, post_method as post, guest,
    is_authenticated, is_unauthenticated
)
from base.forms import (
    LoginForm, SignUPForm, ProfileForm, ExpenseManagerForm,
    ExpenseEntryForm
)
from base.models import User, ExpenseManager
from base.methods import (
    save_registration_form, verify_user, logout)
from django.contrib import messages


class HomePageView(TemplateView):
    @guest
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', None)


@get
@is_unauthenticated
def login(request, methods="GET"):
    form = LoginForm()
    return render(request, 'login.html', {'form': form})


@get
@is_unauthenticated
def signup(request, methods="GET"):
    form = SignUPForm()
    signup = True
    return render(request, 'signup.html', {
        'form': form, 'signup': signup
    })


@get
@is_authenticated
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
@is_unauthenticated
@csrf_exempt
def signupsubmit(request, data):
    registration_status, registration_message = save_registration_form(data)
    if registration_status:
        user_data = {
            'username': str(data.username),
            'password': str(data.password)
        }
        form = LoginForm(user_data)
        return render(request, 'login.html', {'form': form})
    messages.error(
        request,
        'Sorry! Unable to register. Reason: %s' % registration_message)
    return redirect('/account/user/signup')


@post
@is_unauthenticated
@csrf_exempt
def login_api(request, data):
    is_user, user = verify_user(data, request)
    if not is_user:
        return redirect('/account/user/login')
    return redirect('/home')


@is_authenticated
def diary_home(request, user):
    notifications = list()
    manager = False
    expensesManagerForm = ExpenseManagerForm()
    expenseEntryForm = ExpenseEntryForm()
    verify_notif = user.get_verification_notification()
    for notify in verify_notif:
        if len(notify) != 0:
            notifications.append(notify)
    today = datetime.now().date().month
    expense_manager = ExpenseManager.objects.filter(user=user, month__month=today)
    if not expense_manager.exists():
        manager = True
    return render(request, 'user_board.html', {
        'user': user,
        'expensesManagerForm': expensesManagerForm,
        'notifications': notifications,
        'manager': manager
    })


@is_authenticated
def logout_user(request, user):
    logout(request)
    return redirect('/')


@post
@csrf_exempt
def add_expenses(request, data):
    return redirect('/')
