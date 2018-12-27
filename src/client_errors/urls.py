from django.urls import path

from . import views


urlpatterns = [
    path('', views.client_error_handler, name='client_error_handler'),
]
