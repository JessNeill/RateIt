from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Movie, Book, Movie_Rating, Book_Rating, UserProfile
from .forms import UserForm, UserProfileForm, MovieRatingForm, BookRatingForm


# Form tests
class UserFormTest(TestCase):
    def test_user_form_valid(self):
        form_data = {'first_name': 'Test', 'last_name': 'User', 'username': 'testuser@example.com', 'password': 'testpass123'}
        form = UserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_form_invalid(self):
        form_data = {'first_name': 'Test', 'username': 'testuser@example.com', 'password': 'testpass123'}
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())

class UserProfileFormTest(TestCase):
    def test_user_profile_form_valid(self):
        form_data = {}  # Assuming UserProfileForm does not require any fields
        form = UserProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

class MovieRatingFormTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='movierater@example.com', password='movieratepass123')
        self.movie = Movie.objects.create(movie_id=3, title='Matrix', genre='Sci-Fi')

    def test_movie_rating_form_valid(self):
        form_data = {'movie_id': self.movie.movie_id, 'rating': 5, 'comment': 'Great!', 'title': 'Matrix'}
        form = MovieRatingForm(data=form_data)
        self.assertTrue(form.is_valid())

class BookRatingFormTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='bookrater@example.com', password='bookratepass123')
        self.book = Book.objects.create(book_id=3, book_title='Brave New World', genre='Dystopian')

    def test_book_rating_form_valid(self):
        form_data = {'book_id': self.book.book_id, 'rating': 4, 'comment': 'Interesting read.', 'title': 'Brave New World'}
        form = BookRatingForm(data=form_data)
        self.assertTrue(form.is_valid())
