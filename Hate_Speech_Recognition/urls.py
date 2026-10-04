"""Hate_Speech_Recognition URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static

from admins import views as AdminViews
from users import views as UserViews
from users.utility import train


urlpatterns = [
    path('admin/', admin.site.urls),

    path('base', AdminViews.MainBasePage, name='base'),
    path('admin-login', AdminViews.AdminLogin, name='admin-login'),
    path('', AdminViews.UserLoginPage, name='user-login'),
    path('user-register', AdminViews.RegisterUserPage, name='user-register'),

    path('view-users', AdminViews.ViewUsersPage, name='view-users'),
    path('admin-home', AdminViews.AdminHomePage, name='admin-home'),

    path('user-activate/<int:pk>', AdminViews.UserActivateFunction, name='user-activate'),
    path('user-deactivate/<int:pk>', AdminViews.UserDeactivateFunction, name='user-deactivate'),

    # Users Urls
    path('user-home', UserViews.UserHomePage, name='user-home'),
    path('task1', train.task1_view, name='task1'),
    path('matrix', UserViews.ConfusionMatrice, name='matrix'),
    path('prediction', UserViews.hate_speech_predictor, name='prediction'),
    # path('dataset', UserViews.ReadDataset, name='dataset'),
     
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)