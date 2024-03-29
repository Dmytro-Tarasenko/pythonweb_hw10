from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request=request,
                  template_name='app_quotes/index.html',
                  context={'msg': "Quotes app index"})


def authors(request,
            page: int = 1,
            author_id: int = None,
            name: str = None):
    return render(request=request,
                  template_name='app_quotes/index.html',
                  context={'msg': f"Author, page: {page}, id: {author_id}, name: {name}"})


def tags(request,
         tag: str = None,
         page: int = 1):
    return render(request=request,
                  template_name='app_quotes/index.html',
                  context={'msg': f"Tags, page: {page}, tag: {tag}"})


def login(request):
    return render(request=request,
                  template_name='app_quotes/index.html',
                  context={'msg': "Login page"})


def logout(request):
    return render(request=request,
                  template_name='app_quotes/index.html',
                  context={'msg': "Logout handler"})


def register(request):
    return render(request=request,
                  template_name='app_quotes/index.html',
                  context={'msg': "Signup page"})