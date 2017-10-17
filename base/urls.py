from django.conf.urls import url
from django.views.generic import TemplateView   # noqa
import views as base_views


urlpatterns = [
    url(r'^account/user/login', base_views.login, name='login'),  # noqa
    url(r'^account/user/signup', base_views.signup, name='signup'),  # noqa
    url(r'^', base_views.HomePageView.as_view()),
]
