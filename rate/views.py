from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse

def index(request):
    return render(request, 'rate/index.html')

def genres(request):
    return render(request, 'rate/genres.html')

def add_rating(request):
    return render(request, 'rate/add_rating.html')

def my_media(request):
    return render(request, 'rate/my_media.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('rate:index')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'rate/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = User.objects.create_user(username, email, password)
        user.save()
        return redirect('rate:login')
    return render(request, 'rate/register.html')

def restricted(request):
    return render(request, 'rate/restricted.html')

def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

