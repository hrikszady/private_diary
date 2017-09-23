# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from base.models import (
    User, Academic, ParentalInfo, Document, Expense, Memo,

)


class UserAdmin(admin.ModelAdmin):
    """Display all the fields related to
    User class on Admin Panel, Can be seen
    only by Developers.
    """
    list_display = ('name', 'email', 'phone_no', 'created')
    search_fields = ('name', 'phone_no', 'email')
    ordering = ('-created',)
    list_filter = ('name', 'email', 'phone_no')
    # TODOS: Put some actions syntax: ['download']
    # Then define a sub function for the that field.


class AcademicAdmin(admin.ModelAdmin):
    """Dispaly's Academics records for the
    User.
    """
    list_display = (
        'user', 'year_of_passing', 'percentage', 'institute',
        'location'
    )
    search_fields = ('user__name', 'user__phone_no', 'user__email')
    ordering = ('-user__created',)
    list_filter = ('user__name', 'user__email', 'user__phone_no')
    list_display_links = ('user',)
    raw_id_fields = ('user',)


class ParentalInfoAdmin(admin.ModelAdmin):
    """ParentalInfo will be shown only for selected users"""
    list_display = (
        'user', 'fathers_name', 'mothers_name', 'fathers_phone',
        'guardian_phone'
    )
    search_fields = ('user__name', 'user__phone_no', 'user__email')
    ordering = ('-user__created',)
    list_filter = ('user__name', 'user__email', 'user__phone_no')
    list_display_links = ('user',)
    raw_id_fields = ('user',)


class DocumentAdmin(admin.ModelAdmin):
    """ParentalInfo will be shown only for selected users"""
    list_display = (
        'user', 'document_type', 'document_name', 'urgency',
        'digital_validation'
    )
    search_fields = ('user__name', 'user__phone_no', 'user__email')
    ordering = ('-user__created',)
    list_filter = ('user__name', 'user__email', 'user__phone_no')
    list_display_links = ('user',)
    raw_id_fields = ('user',)


class ExpenseAdmin(admin.ModelAdmin):
    """ParentalInfo will be shown only for selected users"""
    list_display = (
        'user', 'amount', 'expense_date', 'category'
    )
    search_fields = ('user__name', 'user__phone_no', 'user__email', 'amount')
    ordering = ('-user__created',)
    list_filter = ('user__name', 'user__email', 'user__phone_no')
    list_display_links = ('user',)
    raw_id_fields = ('user',)


class MemoAdmin(admin.ModelAdmin):
    """ParentalInfo will be shown only for selected users"""
    list_display = (
        'user', 'tag', 'created', 'memo'
    )
    search_fields = ('user__name', 'user__phone_no', 'user__email', 'amount')
    ordering = ('-user__created',)
    list_filter = ('user__name', 'user__email', 'user__phone_no')
    list_display_links = ('user',)
    raw_id_fields = ('user',)


# This is used to register the function on
# Admin panel.
admin.site.register(User, UserAdmin)
admin.site.register(Academic, AcademicAdmin)
admin.site.register(ParentalInfo, ParentalInfoAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Memo, MemoAdmin)
