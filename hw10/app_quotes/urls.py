"""Main app routes"""
from django.urls import path
from . import views

app_name = "app_quotes"

urlpatterns = [
    path('', views.index, name='home'),
    path('authors/', views.authors, name='authors'),
    path('author/<str:name>', views.author_name, name='author'),
    path('tags/', views.tags, name='tags'),
    path('tags/<str:tag>', views.tags, name='tags'),
    path('tags/page/<int:page>', views.tags, name='tags'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.register, name='register')
]
