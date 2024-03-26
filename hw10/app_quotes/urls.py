"""Main app routes"""
from django.urls import path
from . import views

app_name = "app_quotes"

urlpatterns = [
    path('', views.index, name='home')
]
