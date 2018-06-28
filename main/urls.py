"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, re_path
from django.conf.urls import url
from address_book.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^new', create_person),
    url(r'^modify/(?P<id>\d+)/$', modify_person),
    url(r'^delete/(?P<id>\d+)/$', delete_person),
    url(r'^show/(?P<id>\d+)/$', show_person),
    url(r'^', show_all),
]
