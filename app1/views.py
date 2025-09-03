from django.shortcuts import render

# Create your views here.
def renderTemplate(request):
    data = {'nombre': 'Ignacio'}
    return render(request, 'base.html', data)