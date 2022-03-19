"""digiSchool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from digiSchool.loginApp import views as login_view
from digiSchool.profileApp import views as profile_view

urlpatterns = [
    path('admin/', admin.site.urls), path("signup/", login_view.signUpPage),
    path("signup/status/", login_view.signUpPosted), path("login/", login_view.loginPage), path("login/check/", login_view.loginPageCheck),
    path("contact/", login_view.contactPage), path("contact/submit/", login_view.contactPageSubmitted),
    path("profile/<int:userid>/", profile_view.profilePage),
    path("", login_view.homePage) # keep this in last.
]
