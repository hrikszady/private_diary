from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from base.models import User, Guest
from datetime import datetime
from django.http import JsonResponse


@csrf_exempt
def verify_user(self):
    if self.POST:
        username = self.POST.get('username', '')
        password = self.POST.get('password', '')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(
            	self, 'Invalid User ID. Agent doesnot \
                Exists! Please Try Again.')
            return False, self
        if user.check_password(str(password)):
            return True, self
        else:
            messages.error(self, 'Invalid Password ! Please Try Again.')
            return False, self
    messages.error(self, 'Verification Failed')
    return False, self


def logout(self):
    try:
        self.session.flush()
    except KeyError:
        pass
    return True, self


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


def convert_to_dict(self):
    if self.method == 'POST':
        data = dict(self.POST)
        self.POST = {}
        return self, data
    else:
        return JsonResponse({'Error': 'Bas Request'}, status=403)


def save_registration_form(self):
    user, created = User.objects.get_or_create(
        phone_no=self['phone'],
        email=self['email'])
    if not created:
        return created, 'User already exists with phone email combination'
    import pdb; pdb.set_trace()


    return None
