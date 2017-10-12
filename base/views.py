# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import TemplateView
# from methods import *


def login(request):
    return render(request, 'templates/')


class HomePageView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', None)
