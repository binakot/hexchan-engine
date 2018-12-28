from django.urls import path

from . import views


urlpatterns = [
    path('', views.captcha_view, name='captcha_view'),
]
