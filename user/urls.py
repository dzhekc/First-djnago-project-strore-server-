"""store URL Configuration

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
from django.urls import path,include
from django.conf import settings

from user.views import login,registration,logout,UserRegestrationView,UserLoginView, EmailVerificationView

from user.views import UserProfileView,PasswordResetEmailView,PasswordResetEmailConfirm,PasswordComplete



app_name = 'users'

urlpatterns = [
    path('login/',UserLoginView.as_view(),name='login'),
    path('register/',UserRegestrationView.as_view(),name='register'),
    path('profile/<int:pk>',UserProfileView.as_view(), name='profile'),
    path('logout/',logout,name='logout'),
    path('verify/<str:email>/<uuid:code>/',EmailVerificationView.as_view(),name='email_verify'),
    path('password_reset/',PasswordResetEmailView.as_view(),name='password_reset'),
    path('password_confirm/<uidb64>/<token>/',PasswordResetEmailConfirm.as_view(),name='password_confirm'),
    path('new_password_confirm/',PasswordResetEmailConfirm.as_view(),name='new_password_reset'),
    path("new_password_complete", PasswordComplete.as_view(), name='password_complete'),
]


