from django import forms
from django.contrib.auth import get_user_model
from rate.models import UserProfile, Movie_Rating, Book_Rating, Movie, Book

User = get_user_model()

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

class MovieRatingForm(forms.ModelForm):
    title = forms.CharField(max_length=200)
    genre = forms.CharField(max_length=50)

    class Meta:
        model = Movie_Rating
        fields = ['title', 'genre','rating', 'comment', 'image']

class BookRatingForm(forms.ModelForm):
    book_title = forms.CharField(max_length=200)
    genre = forms.CharField(max_length=50)

    class Meta:
        model = Book_Rating
        fields = ['book_title', 'genre','rating', 'comment', 'image']

