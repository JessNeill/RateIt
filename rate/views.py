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

from .forms import UserForm, UserProfileForm
from rate.models import Movie, Movie_Rating, Book, Book_Rating

def index(request):
    context_dict={}
    all_movies = Movie_Rating.objects.all().values()
    movie_id_list=[]
    movies=[] 
    #need to get the average of all movie ratings of each movie
    for movie in all_movies:
        movie_id=movie['movie_id_id']
        if(movie_id in movie_id_list):
            break
        else:
            movie_id_list.append(movie_id)
            total_rating=movie['rating']
            no_ratings=1
            for other_movies in movies:
                if(movie_id==other_movies['movie_id'] and movie['movie_rating_id']!=other_movies['movie_rating_id']):
                    no_ratings=no_ratings+1
                    total_rating=total_rating+other_movies['rating']
            title=Movie.objects.filter(movie_id=movie['movie_id_id'])[0].title
            image=Movie.objects.filter(movie_id=movie['movie_id_id'])[0].picture
            movies.append({'movie_rating_id':movie['movie_rating_id'], 'movie_id':movie_id, 'rating':total_rating/no_ratings, 'title':title, 'image':image})
        
    context_dict['movies']=movies

    all_books = Book_Rating.objects.all().values()
    book_id_list=[]
    books=[]
    
    for book in all_books:
        book_id=book['book_id_id']
        if(book_id in book_id_list):
            break
        
        else:
            book_id_list.append(book_id)
            #comupte the rating
            total_rating=book['rating']
            no_ratings=1
            for other_books in all_books:
                if(book_id==other_books['book_id_id'] and book['book_rating_id']!=other_books['book_rating_id']):
                    no_ratings=no_ratings+1
                    total_rating=total_rating+other_books['rating']
            title=Book.objects.filter(book_id=book['book_id_id'])[0].book_title
            image=Book.objects.filter(book_id=book['book_id_id'])[0].picture
            
            books.append({'book_rating_id':book['book_rating_id'], 'book_id':book_id, 'rating':total_rating/no_ratings, 'title':title, 'image':image})
    context_dict['books']=books
       
    print(context_dict)
    return render(request, 'rate/index.html', context=context_dict)


  def genres(request):
    movies = Movie.objects.all()
    
    genres={'movies':{'Fantasy':[],'Comedy':[],'Romance':[],'Action':[]},
            'books':{'Fantasy':[],'Comedy':[],'Romance':[],'Action':[]}}
    
    for movie in movies:
        title=movie.title
        rating=Movie_Rating.objects.filter(movie_id=movie.movie_id)[0].rating
        #print(Movie_Rating.objects.filter(movie_id=movie.movie_id))
        genre=movie.genre
        movie_id=movie.movie_id
        image=movie.picture
        genres['movies'][str(genre)].append({'movie_id':movie_id, 'title':title, 'rating':rating, 'image':image})
    books = Book.objects.all()
    
    for book in books:
        
        title=book.book_title
        rated_book = Book_Rating.objects.filter(book_id=book.book_id)
        if(len(rated_book)==0):
            #not rated yet: add to dict with null rating
            rating=None
        elif(len(rated_book)>1):
            #more than one rating for the book: need to average rating 
            total_rating=0
            for multiple_rating in rated_book:
                total_rating=total_rating+multiple_rating.rating
            rating=total_rating/len(rated_book)
        genre=book.genre
        book_id=book.book_id
        image=book.picture
        genres['books'][str(genre)].append({'book_id':book_id, 'title':title, 'rating':rating, 'image':image})
    
    print(genres)
    return render(request, 'rate/genres.html', context=genres)

  
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
