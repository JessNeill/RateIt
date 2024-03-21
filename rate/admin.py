# Register your models here.
from django.contrib import admin
from .models import User, UserProfile
from .models import User, UserProfile, Movie, Movie_Rating, Book, Book_Rating

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Movie)
admin.site.register(Movie_Rating)
admin.site.register(Book)
admin.site.register(Book_Rating)