# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid


class User(models.Model):
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
