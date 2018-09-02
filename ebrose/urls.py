#coding=utf-8

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path(r'upload', views.index)
]
