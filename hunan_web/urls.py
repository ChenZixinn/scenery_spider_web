"""hunan_web URL Configuration

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
from django.urls import path

from mainapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('', views.login),
    path('login/', views.login),
    path('register/', views.register),
    path('page/', views.page),

    # path('china_map/', views.china_map),
    # path('pie_goods_weight/', views.pie_goods_weight),
    # path('pie_goods_count/', views.pie_goods_count),
]
