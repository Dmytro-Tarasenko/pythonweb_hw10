from django.shortcuts import render

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
    if request.method == 'POST':
        return render(request=request,
                      template_name='app_quotes/index.html',
                      context={'msg': "Login handler"})
    return render(request=request,
                  template_name='app_quotes/login.html',
                  context={'msg': "Login page"})


def logout(request):
    return render(request=request,
                  template_name='app_quotes/index.html',
                  context={'msg': "Logout handler"})


def register(request):
    return render(request=request,
                  template_name='app_quotes/register.html',
                  context={'msg': "Signup page"})
