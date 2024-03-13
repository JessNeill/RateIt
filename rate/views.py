from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'rate/index.html')

def genres(request):
    return render(request, 'rate/genres.html')

def add_rating(request):
    return render(request, 'rate/add_rating.html')

def my_media(request):
    return render(request, 'rate/my_media.html')

def login(request):
    return render(request, 'rate/login.html')
