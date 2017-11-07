from django.conf.urls import url
from django.views.generic import TemplateView   # noqa
import views as base_views


urlpatterns = [
    url(r'^account/user/login', base_views.login, name='login'),  # noqa
    url(r'^account/user/signup', base_views.signup, name='signup'),  # noqa
    url(r'^account/user/register', base_views.signupsubmit, name='signupsubmit'),  # noqa
    url(r'^account/user/signin', base_views.login_api, name='login_api'),  # noqa
    url(r'^home', base_views.diary_home, name='diary_home'),
    url(r'^', base_views.HomePageView.as_view()),
]
