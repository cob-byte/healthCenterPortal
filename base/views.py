from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def calculate(request):
    x = 1
    y = 2
    return HttpResponse(x+y)

def home(request):
    return HttpResponse('Home page')

def say_hello(request):
    x = calculate()
    return render(request, 'hello.html', {'name': 'Jacob'})