"""TweetToEmoji URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from app import views


# from Processor.Converter import Converter
urlpatterns = [
	url(r'^$', views.Index, name = 'index'),
	path('tweets/<str:q>/', views.GetTweets, name = 'tweets'),
	path('emojis/', views.GetEmojis, name = 'emojis'),
	path('emojis/<str:q>/', views.GetEmojis, name = 'emojis'),
	path('suggest/', views.Suggest, name = 'suggest'),
	path('admin/', admin.site.urls),
]