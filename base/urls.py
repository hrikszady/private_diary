from django.conf.urls import url
from django.views.generic import TemplateView   # noqa
from . import views


urlpatterns = [
    url(r'^', views.HomePageView.as_view()),
]
