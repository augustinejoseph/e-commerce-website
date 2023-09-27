from django.shortcuts import render
from django.urls import path
from . import views
from .views import login

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("active/<uidb64>/<token>/", views.activate, name="activate"),
    path("forgotPassword/", views.forgotPassword, name="forgotPassword"),
    path(
        "resetpasswordValidate/<uidb64>/<token>/",
        views.resetpasswordValidate,
        name="resetpasswordValidate",
    ),
    path("resetPassword/", views.resetPassword, name="resetPassword"),
]
