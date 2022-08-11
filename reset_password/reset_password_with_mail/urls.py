from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reset/', views.send_reset_mail, name='reset'),
    path('reset/confirm/', views.confirm_mail, name='confirm'),
    path('reset/confirm/change/', views.change_mail),
]
