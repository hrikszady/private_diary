from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from base.models import User


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
