from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import get_user_model

class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        
        username = self.normalize_email(username)
        
        if User.objects.filter(username=username).exists():
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
    movie_id = models.IntegerField(unique = True)
    title = models.CharField(max_length = 100)
    genre = models.CharField(max_length = 50)
    picture = models.ImageField(upload_to='images', blank = True)

    def __str__(self):
        return self.title

class Book(models.Model):
    book_id = models.IntegerField(unique = True)
    title = models.CharField(max_length = 100)
    genre = models.CharField(max_length = 50)
    picture = models.ImageField(upload_to='images', blank = True)

    def __str__(self):
        return self.title
    
class Movie_Rating(models.Model):
    #User = get_user_model()
    movie_rating_id = models.IntegerField(unique = True)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    #user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    #user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(max_length = 1)
    comment = models.CharField(max_length = 300)

    class Meta:
        verbose_name_plural = 'Movie Ratings'
        
    def __str__(self):
        return str(self.movie_rating_id)
    
class Book_Rating(models.Model):
    #User = get_user_model()
    book_rating_id = models.IntegerField(unique = True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    #user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.CharField(max_length = 300)

    class Meta:
        verbose_name_plural = 'Book Ratings'

    def __str__(self):
        return str(self.book_rating_id)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    class Meta:
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return self.user.username
