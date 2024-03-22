import os
os.environ['DJANGO_SETTINGS_MODULE']='RateIt.settings'
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'RateIt.settings')
import django
django.setup()
from rate.models import Movie, Movie_Rating, Book, Book_Rating, User
 
def populate():
    media_url=settings.MEDIA_URL
    movies=[{'movie_id':1,'title':'Pulp Fiction','genre':'Action', 'image':os.path.join(media_url,'pulp_fiction.jpg')},
            {'movie_id':2,'title': 'Jaws' ,'genre':'Action', 'image':os.path.join(media_url,'jaws.jpg')}]
    books=[{'book_id':1, 'title':'The Great Gatsby', 'genre':'Fantasy', 'image':os.path.join(media_url,'great_gatsby.jpg')},
           {'book_id':2, 'title':'Circle', 'genre':'Fantasy', 'image':os.path.join(media_url,'circle.jpg')}]
    movie_rating=[{'movie_rating_id':1,'movie_id':1,'user':1, 'rating':9, 'comment':'Loved it, found it really intresting'},
                  {'movie_rating_id':2,'movie_id':2,'user':1, 'rating':6, 'comment':'Its a good movie but not for me, i found it too scary to be enjoyable'}]
    book_rating=[{'book_rating_id':1,'book_id':1,'user':2, 'rating':9, 'comment':'Really good book, found it an intresting read'},
                 {'book_rating_id':2,'book_id':1,'user':1, 'rating':4, 'comment':'Overhyped'}]
    '''users=[{'user_id':1,'first_name':'Jess','last_name':'Neill','email':'hello@gmail.com','password':'supersecret'},
           {'user_id':2,'first_name':'Isla','last_name':'Lase','email':'goodbye@hotmail.com','password':'ubersecret'},
           {'user_id':3,'first_name':'Rosie','last_name':'Posie','email':'rosieposie@gmail.com','password':'nevertelling'}]
    for user_data in users:
       User.objects.get_or_create(
            user_id=user_data['user_id'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            username=user_data['email'],  
            ##email=user_data['email'],
            password=user_data['password']
        )[0]'''
    
    # Populate movies
    for movie_data in movies:
        Movie.objects.get_or_create(
            movie_id=movie_data['movie_id'],
            title=movie_data['title'],
            genre=movie_data['genre'],
            picture=movie_data['image']
        )[0]

    # Populate books
    for book_data in books:
        Book.objects.get_or_create(
            book_id=book_data['book_id'],
            book_title=book_data['title'],
            genre=book_data['genre'],
            picture=book_data['image']
        )[0]

    # Populate movie ratings
    for rating_data in movie_rating:
        Movie_Rating.objects.get_or_create(
            movie_rating_id=rating_data['movie_rating_id'],
            movie_id=Movie.objects.get(movie_id=rating_data['movie_id']),
            user=User.objects.get(user_id=rating_data['user']),
            #username = User.objects.get(username=rating_data['username']),
            rating=rating_data['rating'],
            comment=rating_data['comment']
        )[0]

    for rating_data in book_rating:
        Book_Rating.objects.get_or_create(
            book_rating_id=rating_data['book_rating_id'],
            book_id=Book.objects.get(book_id=rating_data['book_id']),
            user=User.objects.get(user_id=rating_data['user']),
            #user_id=User.objects.get(user_id=rating_data['user_id']),
            rating=rating_data['rating'],
            comment=rating_data['comment']
        )[0]

if __name__ == '__main__':
       print('Starting RateIt population script...')
       populate()
       print('RateIt population script') 