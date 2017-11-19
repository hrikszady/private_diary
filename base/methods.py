from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from base.models import User, Guest, Reference_Number
from datetime import datetime


class FormData(object):
    def get_terms_value(self, request):
        terms = request.POST.get('terms', '')
        if terms == 'on':
            return True
        else:
            return False

    def __init__(self, request):
        self.username = request.POST.get('username', '')
        self.terms = self.get_terms_value(request)
        self.name = request.POST.get('name', '')
        self.country = request.POST.get('country', '')
        self.password = request.POST.get('password', '')
        self.phone = request.POST.get('phone', '')
        self.email = request.POST.get('email', '')


def save_registration_form(self):
    user, created = User.objects.get_or_create(
        phone_no=self.phone)
    if not created:
        return created, 'User already exists with %s.' % str(self.phone)
    if User.objects.filter(email=self.email).exists():
        user.delete()
        return False, 'User already exists with %s.' % str(self.email)
    if User.objects.filter(email=self.username).exists():
        user.delete()
        return False, 'User already exists with %s.' % str(self.username)
    try:
        user.password = self.password
        user.name = self.name
        user.username = self.username
        user.country = self.country
        user.is_approved_terms_and_conditions = self.terms
        user.save()
        message = 'User created! Please Verify yours email and phone.'
        return created, message
    except Exception as e:
        user.delete()
        return False, e


@csrf_exempt
def verify_user(self, request):
    password = self.password
    try:
        user = User.objects.get(username=self.username)
    except User.DoesNotExist:
        try:
            user = User.objects.get(phone_no=self.username)
        except User.DoesNotExist:
            messages.error(
                request, 'Invalid User ID. No user\
                Exists! Please Try Again.')
            return False, self
    if not user.is_email_verified()[0]:
        messages.error(
            request, 'Please. Verify your email !')
        return False, self
    if not user.is_phone_verified()[0]:
        messages.error(
            request, 'Please. Verify your Phone no !')
        return False, self
    if user.check_password(str(password)):
        user.clear_session(request)
        request.session['user_token'] = user.generate_session_id()
        return True, user
    else:
        messages.error(request, 'Invalid Password ! Please Try Again.')
        return False, self
    messages.error(request, 'Invalid! Verification Failed')
    return False, self


def logout(self):
    try:
        self.session.pop('user_token')
    except KeyError:
        self.session.flush()
        return True, self
    return True, self


def verify_user_session(self):
    user_token = self.request.session.get('user_token', None)
    if user_token is not None:
        reference_nos = Reference_Number.objects.all().values('reference_no')
        import bcrypt
        for reference_no in reference_nos:
            if bcrypt.hashpw(
                str(reference_no['reference_no']), str(user_token)
            ) == user_token:
                return True
    return False


def create_guest(ip_address):
    now = datetime.now()
    guest, created = Guest.objects.get_or_create(created=now)
    if created:
        guest.ip_address = ip_address
        guest.save()
    return guest.reference_no


def get_ip_address(self):
    http_ip = self.request.META.get('HTTP_X_FORWARDED_FOR')
    if http_ip:
        ip_address = http_ip.split(',')[0]
    else:
        ip_address = self.request.META.get('REMOTE_ADDR')
    return ip_address


def get_logged_session(self):
    user_token = self.session.get('user_token', None)
    if user_token is not None:
        reference_nos = Reference_Number.objects.all().values('reference_no')
        import bcrypt
        for reference_no in reference_nos:
            if bcrypt.hashpw(
                str(reference_no['reference_no']), str(user_token)
            ) == user_token:
                user = User.objects.get(
                    reference_no=reference_no['reference_no'])
                return True, user
    return False, None
