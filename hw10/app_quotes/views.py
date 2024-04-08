from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import logout as dj_logout
from django.contrib.auth import login as dj_login
from django.urls import reverse

from .models import Author, Quote, Tag


# Create your views here.
def index(request):
    quotes = [{'quote': quote.quote,
               'author': quote.author,
               'tagslist': list(quote.tags.all()),
               'href_name': quote.author.fullname.replace(' ', '_')}
              for quote in Quote.objects.all()]
    return render(request=request,
                  template_name='app_quotes/index.html',
                  context={'quotes': quotes})


def authors(request):
    def make_brief(author: Author) -> str:
        return author.description[:100] + "..."

    authors = list(zip(Author.objects.all(),
                       list(map(make_brief, Author.objects.all())),
                       [author.fullname.replace(' ', '_')
                        for author in Author.objects.all()]
                       )
                   )
    return render(request=request,
                  template_name='app_quotes/authors.html',
                  context={'authors': authors})


def author_name(request, name: str):
    name = name.replace('_', ' ')
    author = Author.objects.get(fullname=name)
    return render(request=request,
                  template_name='app_quotes/author_info.html',
                  context={'author': author})


@login_required(login_url='/login/')
def add_author(request):
    return render(request=request,
                  template_name='app_quotes/addauthor.html',
                  context={})


@login_required(login_url='/login/')
def add_quote(request):
    return render(request=request,
                  template_name='app_quotes/addquote.html',
                  context={})


def tags(request):
    tags_list = [tag for tag in Tag.objects.all() if tag.tag != ""]
    return render(request=request,
                  template_name='app_quotes/tags.html',
                  context={'tags': tags_list})


def quotes(request,
           tag: str):
    res = Quote.objects.filter(tags__tag=tag).all()
    quotes = [{'quote': quote.quote,
               'author': quote.author,
               'tagslist': list(quote.tags.all()),
               'href_name': quote.author.fullname.replace(' ', '_')}
              for quote in res]
    return render(request=request,
                  template_name='app_quotes/tagged-quotes.html',
                  context={'quotes': quotes,
                           'tag': tag})


def login(request):
    if request.user.is_authenticated:
        return redirect("app_quotes:home")
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            print('user is None')
            return render(request=request,
                          template_name='app_quotes/login.html',
                          context={'err': "Invalid credentials"})
        dj_login(request, user)
        next_url = request.POST['next']
        if next_url == 'None':
            next_url = "app_quotes:home"
        print(next_url)
        return redirect(next_url)
    # GET method
    next_url = request.GET.get('next')
    return render(request=request,
                  template_name='app_quotes/login.html',
                  context={'next_url': next_url})


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
