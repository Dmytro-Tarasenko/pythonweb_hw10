from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import logout as dj_logout
from django.contrib.auth import login as dj_login

from .models import Author, Quote, Tag

# Create your views here.
def index(request):
    quotes = [{'quote': quote.quote,
               'author': quote.author,
               'tags': quote.tags.all()}
              for quote in Quote.objects.using('postgre').all()]
    return render(request=request,
                  template_name='app_quotes/index.html',
                  context={'quotes': quotes})


def authors(request,
            page: int = 1,
            author_id: int = None,
            name: str = None):
    authors = Author.objects.using('postgre').all()
    return render(request=request,
                  template_name='app_quotes/authors.html',
                  context={'authors': authors})


def tags(request,
         tag: str = None,
         page: int = 1):
    return render(request=request,
                  template_name='app_quotes/index.html',
                  context={'msg': f"Tags, page: {page}, tag: {tag}"})


def login(request):
    if request.user.is_authenticated:
        return redirect("app_quotes:home")
    if request.method == 'POST':
        print('POST')
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        print(user)
        if user is None:
            print('user is None')
            return render(request=request,
                          template_name='app_quotes/login.html',
                          context={'err': "Invalid credentials"})
        dj_login(request, user)
        return redirect("app_quotes:home")
    print('GET login')
    return render(request=request,
                    template_name='app_quotes/login.html',
                    context={})


def logout(request):
    if request.user.is_authenticated:
        dj_logout(request)
        return redirect('app_quotes:home')
    return render(request=request,
                  template_name='app_quotes/index.html',
                  context={})


def register(request):
    if request.user.is_authenticated:
        return redirect("app_quotes:home")
    if request.method == 'POST':
        data_ = request.POST
        if data_['password'] == data_['password2']:
            try:
                user = User.objects.create_user(username=data_['username'],
                                                email=data_['email'],
                                                password=data_['password'])

            except Exception as e:
                return render(request=request,
                              template_name='app_quotes/register.html',
                              context={'msg': f"User {data_['username']} already exists."})
            user.save()
            return redirect('app_quotes:login')

        return render(request=request,
                      template_name='app_quotes/register.html',
                      context={'msg': "Passwords do not match"})

    return render(request=request,
                  template_name='app_quotes/register.html',
                   context={})
