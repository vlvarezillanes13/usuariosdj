from django.contrib import admin
from django.urls import path
from . import views

app_name = 'users_app'
urlpatterns = [
    path(
        'register/', 
        views.UserRegisterView.as_view(),
        name = 'user-register'
    ),
]
