from django.contrib import admin
#from .models import User,
from .models import UserProfile
from .models import Movie, Book
from .models import Movie_Rating, Book_Rating


admin.site.register(User)
admin.site.register(UserProfile)

admin.site.register(Movie)
admin.site.register(Book)
admin.site.register(Movie_Rating)
admin.site.register(Book_Rating)