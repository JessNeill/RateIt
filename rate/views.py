from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse
from .forms import UserForm, UserProfileForm
from django.contrib.auth import get_user_model

def index(request):
    return render(request, 'rate/index.html')

def genres(request):
    return render(request, 'rate/genres.html')

def add_rating(request):
    return render(request, 'rate/add_rating.html')

def my_media(request):
    return render(request, 'rate/my_media.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('rate:index')
            else:
                return HttpResponse("Your account is inactive.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rate/login.html')

User = get_user_model()

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
            return redirect('rate:login')  # Or any other success URL
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'rate/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    })

def restricted(request):
    return render(request, 'rate/restricted.html')

def user_logout(request):
    logout(request)
    return redirect(reverse('rate:index'))

