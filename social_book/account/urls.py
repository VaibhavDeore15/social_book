from django.urls import path, include
from django.contrib import admin
from .views import *

urlpatterns = [
    path('', user_login, name='login'),
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    
]