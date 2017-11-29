# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.crypto import get_random_string
from django.db import models
from datetime import datetime
import uuid


class User(models.Model):
    """
    Class for user primary details
    to be used when creating CV for users
    and providing offers and premium facility.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_pic = models.FileField(null=True)
    reference_no = models.CharField(default="None", max_length=15)
    username = models.CharField(
        null=True, max_length=10, blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    phone_no = models.CharField(max_length=10)
    alternate_phone_no = models.CharField(
        blank=True, max_length=10, null=True)
    std_code = models.IntegerField(null=True, blank=True)
    COUNTRY_CHOICES = [
        ("india", "IND"), ("pakistan", "PAK"), ("bangaldesh", "BAN"),
        ("srilanka", "SRILNKA"), ("unitedstates", "US"), ("nepal", "NP"),
        ("australia", "AUS"), ("choose country", "Select")
    ]
    country = models.CharField(
        default="Select", choices=COUNTRY_CHOICES, max_length=128)
    email = models.CharField(max_length=64, blank=True, null=True)
    alternate_email = models.CharField(max_length=64, null=True, blank=True)
    pincode = models.IntegerField(blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_phone_no_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    hobbies = models.TextField(null=True, blank=True)
    is_approved_terms_and_conditions = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        try:
            current = User.objects.get(id=self.id)  # noqa
        except User.DoesNotExist:
            if self.reference_no == "None":
                self.reference_no = self.get_or_create_reference_no()
        super(User, self).save(*args, **kwargs)

    @staticmethod
    def check_password(self, password):
        """Check hased password. Using bcrypt,
        the salt is saved into the hash itself
        """
        import bcrypt
        credential = Credentials.objects.get(user=self)
        return bcrypt.hashpw(
            password, str(credential.password)) == str(credential.password)

    def get_or_create_reference_no(self):
        reference_no = get_random_string(
            15, allowed_chars='ABCDEFGHITUVWXYZ0123456789')
        while (
            Reference_Number.objects.filter(
                reference_no=reference_no)).exists():
            reference_no = get_random_string(
                15, allowed_chars='ABCDEFGHITUVWXYZ0123456789')
        Reference_Number.objects.create(
            user=self, reference_no=reference_no,
            purpose='User Registration')
        return reference_no

    def generate_session_id(self):
        import bcrypt
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(str(self.reference_no), salt)

    def clear_session(self, request):
        request.session.pop('guest_id', '')
        request.session.pop('user_token', '')
        return True

    def is_email_verified(self):
        grace_time = (datetime.now().date() - self.created.date()).days
        if grace_time > 7 and not self.is_email_verified:
            # Replace 'or' with 'and'
            return False, 7 - grace_time
        return True, 7 - grace_time

    def is_phone_verified(self):
        grace_time = (datetime.now().date() - self.created.date()).days
        if grace_time > 45 and not self.is_phone_no_verified:
            # Replace 'or' with 'and'
            return False, 45 - grace_time
        return True, 45 - grace_time

    def get_verification_notification(self):
        now = str(datetime.now().time()).split('.')[0]
        email_notification = []
        phone_notification = []
        phone_grace = self.is_phone_verified()[1]
        email_grace = self.is_email_verified()[1]
        if not self.is_phone_no_verified:
            # TODOs: Check also from user instance(is_phone_no_verified)
            # For development its ok
            phone_notification.extend(['Verify Phone', True,
                'Hi, Your email is unverifed, Please verify your phone in :%s day(s) ' % phone_grace, now])  # noqa
        if not self.is_email_verified:
            # TODOs: Check also from user instance(is_email_verified)
            # For development its ok
            email_notification.extend(['Verify Email', True,
                'Hi, Your email is unverifed, Please verify your email in :%s day(s)' % email_grace, now])  # noqa
        return phone_notification, email_notification


class Credentials(models.Model):
    """Tampering with this model result in unable to login
    Consult core-developer to know more about this login panel
    """
    user = models.ForeignKey('User')
    password = models.CharField(max_length=520)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        try:
            current = Credentials.objects.get(user=self.user)  # noqa
            self.password = self.get_hashed_password(str(self.password))
        except Credentials.DoesNotExist:
            self.password = self.get_hashed_password(str(self.password))
        super(Credentials, self).save(*args, **kwargs)

    def get_hashed_password(self, password):
        """Hash a password for the first time
        Using bcrypt, the salt is saved into the hash itself
        """
        import bcrypt
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password, salt)


class Academic(models.Model):
    """Stores for Academics details for registered users"""
    user = models.ForeignKey('User')
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
    user = models.ForeignKey('User')
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
    user = models.ForeignKey('User')
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
    user = models.ForeignKey('User')
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
    created = models.DateTimeField(auto_now_add=True)


class Memo(models.Model):
    """
    Create a memo for works
    """
    user = models.ForeignKey('User')
    memo = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(blank=True, null=True, max_length=8)


class Donation(models.Model):
    """
    Records donation made by user
    """
    user = models.ForeignKey('User')
    transaction_id = models.CharField(
        blank=False, default=None, max_length=64)
    amount = models.FloatField(blank=False, default=0)
    comments = models.TextField()
    transaction_mode = models.CharField(
        blank=False, default=None, max_length=64)
    created = models.DateTimeField(auto_now_add=True)


class LastAction(models.Model):
    """
    Tracks user's LastAction
    """
    user = models.ForeignKey('User')
    action = models.CharField(blank=False, max_length=128)
    created = models.DateTimeField(auto_now_add=True)


class Reference_Number(models.Model):
    """Stores each reference_no alloted details"""
    reference_no = models.CharField(max_length=15)
    user = models.ForeignKey('User', blank=True, null=True)
    guest = models.ForeignKey('Guest', blank=True, null=True)
    genration_date = models.DateTimeField(auto_now_add=True)
    purpose = models.CharField(max_length=128)


class Guest(models.Model):
    """Records Guest details"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference_no = models.CharField(max_length=15)
    ip_address = models.CharField(max_length=32, blank=True)
    created = models.DateTimeField(auto_now_add=False)

    def save(self, *args, **kwargs):
        try:
            current = Guest.objects.get(id=self.id)
            if current.reference_no == self.reference_no:
                super(Guest, self).save(*args, **kwargs)
            self.reference_no = self.get_or_create_reference_no()
        except Guest.DoesNotExist:
            self.reference_no = self.get_or_create_reference_no()
        super(Guest, self).save(*args, **kwargs)

    def get_or_create_reference_no(self):
        reference_no = get_random_string(
            15, allowed_chars='ABCDEFGHITUVWXYZ0123456789')
        while (
            Reference_Number.objects.filter(
                reference_no=reference_no)).exists():
            reference_no = get_random_string(
                15, allowed_chars='ABCDEFGHITUVWXYZ0123456789')
        Reference_Number.objects.create(
            guest=self, reference_no=reference_no,
            purpose='User Registration')
        return reference_no

class Work_Experience(models.Model):
    """docstring for Work_Experience"""
    user = models.ForeignKey('User')
    organization = models.CharField(max_length=64)
    designation = models.CharField(max_length=64)
    joing_date = models.DateField(null=True,blank=False)
    leaving_date = models.DateField(null=True,blank=False)
    Role = models.CharField(max_length=64)


class Extra_Curricular_Activities(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    achievement = models.CharField(max_length=64)
    source = models.CharField(max_length=128)
    details = models.TextField()
