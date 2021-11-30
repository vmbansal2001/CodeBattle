"""CodeBattle URL Configuration

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
from django.urls import path, include
from BattleZone import views
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [
    path('', views.index, name='home'), #Home Page
    path('sign_in', views.sign_in, name='sign_in'), #Sign in page
    path('welcomeNote',views.welcomeNote, name='welcome'), #Welcome home page
    path('room',views.room, name='room'), #Room page (create or enter room)
    path('createRoom',views.createRoom, name='createRoom'), #Create room page
    path('enterRoom',views.enterRoom, name='enterRoom'), #Enter a room page
    path('playersPage',views.playersPage, name='playersPage'), #Players page
    path('signUp',views.signUp, name='signUp'), #Sign Up page
    path('logout', views.logoutUser, name='logout'), #Logout User
    path('about', views.about, name='about'), #About Page
    path('ide', views.ide, name='ide'), #IDE
    path('executeCode', views.executeCode, name='executeCode'), #To execute IDE code
    path('practice', views.practice, name='practice'),
    path('favicon.ico',
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
]
