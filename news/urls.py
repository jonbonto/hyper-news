from django.urls import path, include
from django.shortcuts import render
from .views import get_news, index, create_news


urlpatterns = [
    path('', index),
    path('<int:id>/', get_news),
    path('create/', create_news)
]
