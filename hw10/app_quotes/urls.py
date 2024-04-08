"""Main app routes"""
from django.urls import path
from . import views

app_name = "app_quotes"

urlpatterns = [
    path('', views.index, name='home'),
    path('authors/', views.authors, name='authors'),
    path('author/<str:name>', views.author_name, name='author'),
    path('addauthor/', views.add_author, name='addauthor'),
    path('addquote/', views.add_quote, name='addquote'),
    path('tags/', views.tags, name='tags'),
    path('quotes/<str:tag>', views.quotes, name='quotes'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.register, name='register')
]
