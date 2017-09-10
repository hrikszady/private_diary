# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid


class User(models.Model):
    """ Class for user primary details
    to be used when creating CV for users
    and providing offers and premium facility.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference_no = models.CharField(default=None, max_length=10)
    name = models.CharField(max_length=20)
    phone_no = models.IntegerField(
        default=0000000000, blank=False)
    alternate_phone_no = models.IntegerField(default=0000000000)
    std_code = models.IntegerField(default=000000)
    COUNTRY_CHOICES = [
        ("india", "IND"), ("pakistan", "PAK"), ("bangaldesh", "BAN"),
        ("srilanka", "SRILNKA"), ("unitedstates", "US"), ("nepal", "NP"),
        ("australia", "AUS"), ("choose country", "Select")
    ]
    country = models.CharField(
        default="Select", choices=COUNTRY_CHOICES, max_length=128)
    email = models.CharField(max_length=32)
    alternate_email = models.CharField(max_length=32)
    pincode = models.IntegerField(blank=True, default="Not Provided")
    address = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_phone_no_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    hobbies = models.TextField(null=True, blank=True)


class Academics(models.Model):
    """Stores for Academics details for registered users"""
    user = models.ForeignKey('user')
    year_of_passing = models.DateTimeField(null=True, blank=True)
    percentage = models.FloatField(default=0)
    institute = models.CharField(default=256, max_length=256)
    location = models.CharField(default=128, max_length=64)


class ExtraUserInfo(object):
    """Class ExtraPersonalInfo is created for those
    users who wish to create resume, they have to fill
    these extra options"""
    user = models.ForeignKey('user')
    fathers_name = models.CharField(blank=False, max_length=64)
    mothers_name = models.CharField(blank=True, max_length=64)
    fathers_phone = models.CharField(blank=False, max_length=64)
