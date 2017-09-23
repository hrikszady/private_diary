# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.crypto import get_random_string
from django.db import models
import uuid


class User(models.Model):
    """
    Class for user primary details
    to be used when creating CV for users
    and providing offers and premium facility.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference_no = models.CharField(default="None", max_length=10)
    username = models.CharField(
        default=None, max_length=10)
    password = models.CharField(max_length=512)
    name = models.CharField(max_length=20)
    phone_no = models.CharField(
        default=0000000000, blank=False, max_length=10)
    alternate_phone_no = models.CharField(
        default=0000000000, blank=True, max_length=10)
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
    is_approved_terms_and_conditions = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        try:
            current = User.objects.get(id=self.id)
            if not current.check_password(str(self.password)):
                self.password = self.get_hashed_password(str(self.password))
        except User.DoesNotExist:
            if self.reference_no == "None":
                temp_ref = get_random_string(
                    10, allowed_chars='ABCDEFGHITUVWXYZ0123456789')
                users = User.objects.filter(reference_no=temp_ref)
                while users.exists():
                    temp_ref = get_random_string(
                        10, allowed_chars='ABCDEFGHITUVWXYZ0123456789') # noqa
                self.reference_no = temp_ref
            self.password = self.get_hashed_password(str(self.password))
        super(User, self).save(*args, **kwargs)

    def get_hashed_password(self, password):
        """Hash a password for the first time
        Using bcrypt, the salt is saved into the hash itself
        """
        import bcrypt
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password, salt)

    def check_password(self, password):
        """Check hased password. Using bcrypt,
        the salt is saved into the hash itself
        """
        import bcrypt
        return bcrypt.hashpw(
            password, str(self.password)) == str(self.password)


class Academic(models.Model):
    """Stores for Academics details for registered users"""
    user = models.ForeignKey('user')
    year_of_passing = models.DateTimeField(null=True, blank=True)
    percentage = models.FloatField(default=0)
    institute = models.CharField(default=None, max_length=256)
    location = models.CharField(default=None, max_length=64)


class ParentalInfo(models.Model):
    """
    Class ExtraPersonalInfo is created for those
    users who wish to create resume, they have to fill
    these extra options
    """
    user = models.ForeignKey('user')
    fathers_name = models.CharField(blank=False, max_length=32)
    mothers_name = models.CharField(blank=True, max_length=32)
    fathers_phone = models.CharField(
        default=0000000000, blank=False, max_length=10)
    guardian_phone = models.CharField(
        default=0000000000, blank=False, max_length=10)


class Document(models.Model):
    """
    Stores Documents for users, if case they need
    user can download their documents
    """
    user = models.ForeignKey('user')
    document_type = models.CharField(blank=False, max_length=16)
    document_name = models.CharField(blank=False, max_length=64)
    URGENCY_CHOICES = [
        ("select", "CHOOSE"), ("top", "TOP"), ("medium", "MEDIUM"),
        ("high", "HIGH"), ("urgent", "URGENT")
    ]
    urgency = models.CharField(
        default="select", choices=URGENCY_CHOICES, max_length=12)
    filename = models.CharField(blank=False, max_length=32)
    digital_validation = models.BooleanField(default=False)


class Expense(models.Model):
    """
    User can keep track for their expenses
    """
    user = models.ForeignKey('user')
    amount = models.FloatField(default=0)
    expense_date = models.DateTimeField(auto_now_add=False)
    CATEGORY_CHOICES = [
        ("select", "CHOOSE"), ("food", "FOOD"),
        ("bill_payments", "BILL & PAYMENTS"),
        ("shopping_purchases", "SHOPPING & PURCHASES"),
        ("lended", "LENDING"), ("fare", "FARE"),
        ("donation", "DONATION"), ("fees", "FEES"),
        ("fine", "FINE"), ("movie", "MOVIE")
    ]
    category = models.CharField(
        default="select", choices=CATEGORY_CHOICES, max_length=12)
    description = models.TextField()
    comment = models.CharField(blank=True, null=True, max_length=64)


class Memo(models.Model):
    """
    Create a memo for works
    """
    user = models.ForeignKey('user')
    memo = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(blank=True, null=True, max_length=8)


class Donation(models.Model):
    """
    Records donation made by user
    """
    user = models.ForeignKey('user')
    transaction_id = models.CharField(blank=False, default=None, max_length=64)
    amount = models.FloatField(blank=False, default=0)
    comments = models.TextField()
    transaction_mode = models.CharField(
        blank=False, default=None, max_length=64)
    created = models.DateTimeField(auto_now_add=True)


class LastAction(object):
    """
    Tracks user's LastAction
    """
    user = models.ForeignKey('user')
    action = models.CharField(blank=False, max_length=128)
    created = models.DateTimeField(auto_now_add=True)
