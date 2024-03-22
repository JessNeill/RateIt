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
    # Aggregate average rating for each movie
    movie_ratings = (
        Movie_Rating.objects
        .values('movie')
        .annotate(average_rating=Avg('rating'))
        .order_by('-average_rating')[:10]  # Assuming you want the top 10
    )

    # Get corresponding movie details
    movies = [
        {
            'movie_id': rating['movie'],
            'rating': rating['average_rating'],
            'title': Movie.objects.get(pk=rating['movie']).title,
            'image': Movie.objects.get(pk=rating['movie']).picture.url if Movie.objects.get(pk=rating['movie']).picture else None,
        }
        for rating in movie_ratings
    ]

    # Aggregate average rating for each book
    book_ratings = (
        Book_Rating.objects
        .values('book')
        .annotate(average_rating=Avg('rating'))
        .order_by('-average_rating')[:10]  # Assuming you want the top 10
    )

    # Get corresponding book details
    books = [
        {
            'book_id': rating['book'],
            'rating': rating['average_rating'],
            'title': Book.objects.get(pk=rating['book']).book_title,
            'image': Book.objects.get(pk=rating['book']).picture.url if Book.objects.get(pk=rating['book']).picture else None,
        }
        for rating in book_ratings
    ]

    # Create context dictionary
    context = {
        'movies': movies,
        'books': books,
    }

    # Pass context dictionary to the template
    return render(request, 'rate/index.html', context=context)


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
    
    return render(request, 'rate/genres.html', {
        'movies': movies,
        'books': books
    })

  
@login_required
def add_rating(request):
    if request.method == 'POST':
        media_type = request.POST.get('media_type')
        genre = request.POST.get('genre')
        form = None

        if media_type == 'movie':
            form = MovieRatingForm(request.POST, request.FILES)
            title = form['title'].value()
        elif media_type == 'book':
            form = BookRatingForm(request.POST, request.FILES)
            book_title = form['book_title'].value()
        else:
            messages.error(request, 'Invalid media type')
            return redirect('rate:index')

        if form.is_valid():
            rating_instance = form.save(commit=False)
            if media_type == 'movie':
                media, created = Movie.objects.get_or_create(title=title, defaults={'genre': genre})
                rating_instance.movie = media
            elif media_type == 'book':
                media, created = Book.objects.get_or_create(book_title=book_title, defaults={'genre': genre})
                rating_instance.book = media

            rating_instance.user = request.user
            rating_instance.save()
            messages.success(request, 'Your rating has been added successfully!')
            return redirect('rate:index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect('rate:add_rating')

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
