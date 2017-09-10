# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from base.models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    """Display all the fields related to
    User class on Admin Panel, Can be seen
    only by Developers.
    """
    list_display = ("name", "email", "phone_no", "created")
    search_fields = ('name', 'phone_no', "email")
    ordering = ('-created',)
    list_filter = ("name", "email", "phone_no")
    # TODOS: Put some actions syntax: ['download']
    # Then define a sub function for the that field.


# This is used to register the function on
# Admin panel.
admin.site.register(User, UserAdmin)
