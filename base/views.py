# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from methods import *


def login(request):
	return render(request, 'templates/')
