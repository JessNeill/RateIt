from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rate.forms import UserForm, UserProfileForm, MovieRatingForm, BookRatingForm
from rate.models import Movie, Movie_Rating, Book, Book_Rating
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

from .forms import UserForm, UserProfileForm
from rate.models import Movie, Movie_Rating, Book, Book_Rating

def index(request):
    # Get top 10 movies based on average rating
    top_movies = Movie.objects.annotate(avg_rating=Avg('movie_rating__rating')).order_by('-avg_rating')[:10]

    # Get top 10 books based on average rating
    top_books = Book.objects.annotate(avg_rating=Avg('book_rating__rating')).order_by('-avg_rating')[:10]

    context = {
        'top_movies': [{
            'title': movie.title,
            'avg_rating': movie.avg_rating,
            'image_url': movie.picture.url if movie.picture else None,
        } for movie in top_movies],

        'top_books': [{
            'title': book.book_title,
            'avg_rating': book.avg_rating,
            'image_url': book.picture.url if book.picture else None,
        } for book in top_books],
    }

    return render(request, 'rate/index.html', context)



def genres(request):
    movies = (
        Movie.objects
        .annotate(average_rating=Avg('movie_rating__rating'))
        .order_by('genre', '-average_rating')
    )
    
    books = (
        Book.objects
        .annotate(average_rating=Avg('book_rating__rating'))
        .order_by('genre', '-average_rating')
    )
    print(movies)
    
    return render(request, 'rate/genres.html', {
        'movies': movies,
        'books': books
    })

  
@login_required
def add_rating(request):
    if request.method == 'POST':
        media_type = request.POST.get('media_type')
        form = MovieRatingForm(request.POST, request.FILES) if media_type == 'movie' else BookRatingForm(request.POST, request.FILES)

        if form.is_valid():
            title = form.cleaned_data.get('title') if media_type == 'movie' else form.cleaned_data.get('book_title')
            genre = form.cleaned_data.get('genre')
            image = request.FILES.get('image')  # Handle the uploaded file
            
            rating_instance = form.save(commit=False)
            if media_type == 'movie':
                media, created = Movie.objects.get_or_create(title=title, defaults={'genre': genre})
                if created and image:
                    media.picture = image
                    media.save()
            elif media_type == 'book':
                media, created = Book.objects.get_or_create(book_title=title, defaults={'genre': genre})
                if created and image:
                    media.picture = image
                    media.save()

            rating_instance.user = request.user
            if media_type == 'movie':
                rating_instance.movie = media
            elif media_type == 'book':
                rating_instance.book = media
            rating_instance.save()

            messages.success(request, 'Your rating has been added successfully!')
            return redirect('rate:index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return render(request, 'rate/add_rating.html', {
                'movie_form': form if media_type == 'movie' else MovieRatingForm(),
                'book_form': form if media_type == 'book' else BookRatingForm(),
                'media_type': media_type,
            })
    else:
        return render(request, 'rate/add_rating.html', {
            'movie_form': MovieRatingForm(),
            'book_form': BookRatingForm()
        })

    

@login_required
def my_media(request):
    user = request.user
    my_movie_ratings = Movie_Rating.objects.filter(user=user).select_related('movie')
    my_book_ratings = Book_Rating.objects.filter(user=user).select_related('book')
    
    context = {
        'my_movies': [{
            'title': mr.movie.title,
            'genre': mr.movie.genre,
            'image': mr.movie.picture.url if mr.movie.picture else None,
            'rating': mr.rating,
            'comment': mr.comment
        } for mr in my_movie_ratings],
        
        'my_books': [{
            'title': br.book.book_title,
            'genre': br.book.genre,
            'image': br.book.picture.url if br.book.picture else None,
            'rating': br.rating,
            'comment': br.comment
        } for br in my_book_ratings]
    }

    print(context)
    
    return render(request, 'rate/my_media.html', context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, "You are now logged in.")
                return redirect('rate:index')
            else:
                messages.warning(request, "Your account is inactive.")
                return redirect('rate:login')
        else:
            messages.error(request, "Invalid login details supplied.")
            return redirect('rate:login')
    else:
        return render(request, 'rate/login.html')

User = get_user_model()

def register(request):
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

            messages.success(request, "You have successfully registered.")
            return redirect('rate:login')
        else:
            errors = []
            for form in [user_form, profile_form]:
                for field, error_messages in form.errors.items():
                    for error in error_messages:
                        errors.append(f"{field}: {error}")
            for error in errors:
                messages.error(request, error)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rate/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

def restricted(request):
    return render(request, 'rate/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rate:index'))
