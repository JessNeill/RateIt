from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    user_id = models.IntegerField(unique = True)
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    email = models.CharField(max_length = 50, unique = True)
    password = models.CharField(max_length = 20)

    def __str__(self):
        return self.name
    
class Movie(models.Model):
    movie_id = models.IntegerField(unique = True)
    title = models.CharField(max_length = 100)
    genre = models.CharField(max_length = 50)
    picture = models.ImageField(upload_to='images', blank = True)

    def __str__(self):
        return self.name

class Book(models.Model):
    book_id = models.IntegerField(unique = True)
    book_title = models.CharField(max_length = 100)
    genre = models.CharField(max_length = 50)
    picture = models.ImageField(upload_to='images', blank = True)

    def __str__(self):
        return self.name
    
class Movie_Rating(models.Model):
    movie_rating_id = models.IntegerField(unique = True)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(max_length = 1)
    comment = models.CharField(max_length = 300)

    def __str__(self):
        return self.name
    
class Book_Rating(models.Model):
    book_rating_id = models.IntegerField(unique = True)
    book_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(max_length = 1)
    comment = models.CharField(max_length = 300)

    def __str__(self):
        return self.name
