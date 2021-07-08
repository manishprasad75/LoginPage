"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from users import views as usersView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', usersView.index, name="index"),
    path('login/', usersView.loginPage, name="login"),
    path('logout/', usersView.logoutPage, name="logout"),
    path('register/', usersView.registerationPage, name="register"),
    path('verification/', usersView.verification, name="email-verification"),
    path('passwordReset/', usersView.password_reset, name="password-reset"),
    path('passwordResetConform/', usersView.password_check, name="password-reset-conf"),
    path('passwordResetForm/', usersView.password_set_form, name="password-reset-form"),
]
