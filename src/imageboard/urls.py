from django.urls import path

from . import views


urlpatterns = [
    path('', views.start_page, name='start_page'),
    path('error/', views.error_page, name='error_page'),
    path('<str:board_hid>/', views.board_page, name='board_page'),
    path('<str:board_hid>/catalog/', views.catalog_page, name='catalog_page'),
    path('<str:board_hid>/<str:thread_hid>/', views.thread_page, name='thread_page'),
]
