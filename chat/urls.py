from re import template
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.create, name='create'),
    path('home/', views.home, name='home'),
    path('<str:room>/', views.room, name='room'),
    path('home/checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('logout', views.logout, name='logout'),
]