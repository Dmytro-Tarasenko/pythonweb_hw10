from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request=request,
                  template_name='app_quotes/index.html',
                  context={'msg': "Quotes app index"})
