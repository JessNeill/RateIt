from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import UserForm, UserProfileForm
from rate.models import Movie, Movie_Rating, Book, Book_Rating

def index(request):
    return render(request, 'rate/index.html')

def genres(request):
    return render(request, 'rate/genres.html')

@login_required
def add_rating(request):
    return render(request, 'rate/add_rating.html')

@login_required
def my_media(request):
    context_dict={}
    my_br_list = Book_Rating.objects.filter(user_id=request.user.user_id).values()
    context_dict['my_books']=my_br_list
 
    for br in my_br_list:
        title = Book.objects.filter(book_id=br.book_id).book_title
        genre = Book.objects.filter(book_id=br.book_id).genre
        image = Book.objects.filter(book_id=br.book_id).image
        br['title']=title
        br['genre']=genre
        br['image']=image
       
    my_mr_list = Movie_Rating.objects.filter(user_id=request.user.user_id).values() ##it might be request.user.user_id but hopefully this is the right code for getting the current user id (request.user.id) the tutor wasnt all that confident
    context_dict['my_movies'] = my_mr_list
   
    for mr in my_mr_list:
        title = Movie.objects.filter(movie_id=mr.movie_id).title
        genre = Movie.objects.filter(movie_id=mr.movie_id).genre
        image = Movie.objects.filter(movie_id=mr.movie_id).image
        mr['title']=title
        mr['genre']=genre
        mr['image']=image
   
    ##context_dict={'my_movies':{'movie_rating':6,'movie_id':2, 'user_id':4, 'rating': 6, 'comment': 'nice', 'title':"Oppenhimer", 'genre':"comedy", 'image':"eognoirad"},{...},{...}...}
  
    return render(request, 'rate/my_media.html', context=context_dict)

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

#is this supposed to be here??
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
            return redirect('rate:login')
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

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rate:index'))

