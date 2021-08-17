"""charity_donation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path

from main import views

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', views.LandingPage.as_view(), name="landing_page"),
    path('add_donation/', views.AddDonation.as_view(), name='add_donation'),
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Register.as_view(), name='register'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('settings/<int:pk>/', views.ProfileSettings.as_view(), name='settings'),
    path('settings_check/', views.SettingsCheck.as_view(), name='settings_check'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('form_confirmation/', views.FormConfirmation.as_view(), name='form_confirmation'),
    path('archive/<int:pk>/', views.Archive.as_view(), name='archive'),
]
