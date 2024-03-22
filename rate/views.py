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
        form = MovieRatingForm(request.POST, request.FILES) if request.POST.get('media_type') == 'movie' else BookRatingForm(request.POST, request.FILES)

        if form.is_valid():
            title = form.cleaned_data.get('title')
            rating_instance = form.save(commit=False)
            rating_instance.user = request.user

            if request.POST.get('media_type') == 'movie':
                movie, created = Movie.objects.get_or_create(title=title)
                rating_instance.movie_id = movie
            else:
                book, created = Book.objects.get_or_create(title=title)
                rating_instance.book_id = book

            rating_instance.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        movie_form = MovieRatingForm()
        book_form = BookRatingForm()
        return render(request, 'rate/add_rating.html', {
            'movie_form': movie_form,
            'book_form': book_form
        })


@login_required
def my_media(request):
    context_dict={}
    my_br_list = Book_Rating.objects.all().values()
    context_dict['my_books']=my_br_list
 
    for br in my_br_list:
        
        title = Book.objects.filter(book_id=br['book_id_id'])[0].book_title
        genre = Book.objects.filter(book_id=br['book_id_id'])[0].genre
        image = Book.objects.filter(book_id=br['book_id_id'])[0].picture
        br['title']=title
        br['genre']=genre
        br['image']=image
       
    my_mr_list = Movie_Rating.objects.all().values() 
    context_dict['my_movies'] = my_mr_list
    
    for mr in my_mr_list:
        title = Movie.objects.filter(movie_id=mr['movie_id_id'])[0].title
        genre = Movie.objects.filter(movie_id=mr['movie_id_id'])[0].genre
        image = Movie.objects.filter(movie_id=mr['movie_id_id'])[0].picture
        mr['title']=title
        mr['genre']=genre
        mr['picture']=image
        print(mr['picture'])
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
