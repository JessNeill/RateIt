from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import get_user_model

class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        
        username = self.normalize_email(username)
        
        user_model = get_user_model()
        if user_model.objects.filter(username=username).exists():
            raise ValueError('A user with this username already exists')
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.username
      
class Movie(models.Model):
    GENRE_CHOICES = (
        ('Crime', 'Crime'),
        ('Thriller', 'Thriller'),
        ('Others', 'Others'),
    )
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 100)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    picture = models.ImageField(upload_to='images', blank = True)

    def __str__(self):
        return self.title

class Book(models.Model):
    GENRE_CHOICES = (
        ('Fantasy', 'Fantasy'),
        ('Tragedy', 'Tragedy'),
        ('Others', 'Others'),
    )
    book_id = models.AutoField(primary_key=True)
    book_title = models.CharField(max_length = 100)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    picture = models.ImageField(upload_to='images', blank = True)

    def __str__(self):
        return self.book_title
    
class Movie_Rating(models.Model):
    movie_rating_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField()
    comment = models.CharField(max_length = 300)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f"{self.movie.title} - {self.user.username}"


class Book_Rating(models.Model):
    book_rating_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField()
    comment = models.CharField(max_length = 300)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f"{self.book.book_title} - {self.user.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    class Meta:
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return self.user.username
