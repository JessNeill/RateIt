from django.contrib.auth.models import Permission
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Movie, Book, Movie_Rating, Book_Rating, UserProfile
from .forms import UserForm, UserProfileForm, MovieRatingForm, BookRatingForm
from django.urls import reverse
from django.test import Client

User = get_user_model()

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
        form_data = {}  
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

# Model tests

class UserModelTest(TestCase):
    def test_user_str(self):
        user = User.objects.create_user(username='testuser@example.com', password='testpass123', first_name='Test', last_name='User')
        self.assertEqual(str(user), 'testuser@example.com')

class MovieModelTest(TestCase):
    def test_movie_str(self):
        movie = Movie.objects.create(movie_id=1, title='Inception', genre='Action')
        self.assertEqual(str(movie), 'Inception')

class BookModelTest(TestCase):
    def test_book_str(self):
        book = Book.objects.create(book_id=1, book_title='The Great Gatsby', genre='Fiction')
        self.assertEqual(str(book), 'The Great Gatsby')

class MovieRatingModelTest(TestCase):
    def test_movie_rating_str(self):
        user = User.objects.create_user(username='ratinguser@example.com', password='ratingpass123')
        movie = Movie.objects.create(movie_id=2, title='Interstellar', genre='Sci-Fi')
        movie_rating = Movie_Rating.objects.create(movie_rating_id=1, movie_id=movie, user=user, rating=5, comment='Great film!')
        self.assertEqual(str(movie_rating), '1')

class BookRatingModelTest(TestCase):
    def test_book_rating_str(self):
        user = User.objects.create_user(username='bookluvr123@email.com', password='ilovebooks456')
        book = Book.objects.create(book_id=2, title='1984', genre='Dystopian')
        book_rating = Book_Rating.objects.create(book_rating_id=1, book_id=book, user=user, rating=4, comment='Decent read')
        self.assertEqual(str(book_rating), '1')

class UserProfileModelTest(TestCase):
    def test_user_profile_str(self):
        user = User.objects.create_user(username='profileuser@example.com', password='profilepass123')
        user_profile = UserProfile.objects.create(user=user)
        self.assertEqual(str(user_profile), 'profileuser@example.com')

# View tests
class IndexViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('rate:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rate/index.html')

class GenresViewTest(TestCase):
    def test_genres_view(self):
        response = self.client.get(reverse('rate:genres'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rate/genres.html')

class AddRatingViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser@example.com', password='testpass123')
        self.client = Client()

    def test_add_rating_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('rate:add_rating'))
        self.assertRedirects(response, '/rate/login/?next=/rate/add_rating/')
    
    def test_add_rating_logged_in_renders_correct_template(self):
        self.client.login(username='testuser@example.com', password='testpass123')
        response = self.client.get(reverse('rate:add_rating'))
        self.assertEqual(str(response.context['user']), 'testuser@example.com')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rate/add_rating.html')

class MyMediaViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser@example.com', password='testpass123')
        self.client = Client()
    
    def test_my_media_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('rate:my_media'))
        self.assertRedirects(response, '/rate/login/?next=/rate/my_media/')

    def test_my_media_logged_in_renders_correct_template(self):
        self.client.login(username='testuser@example.com', password='testpass123')
        response = self.client.get(reverse('rate:my_media'))
        self.assertEqual(str(response.context['user']), 'testuser@example.com')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rate/my_media.html')

class UserLoginLogoutTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser@example.com', password='testpass123')
        self.client = Client()

    def test_login_page(self):
        response = self.client.get(reverse('rate:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rate/login.html')
    
    def test_login_logout_functionality(self):
        login = self.client.login(username='testuser@example.com', password='testpass123')
        self.assertTrue(login)
        response = self.client.get(reverse('rate:logout'))
        self.assertRedirects(response, reverse('rate:index'))

class RegistrationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_register_view(self):
        response = self.client.get(reverse('rate:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rate/register.html')
    
    def test_register_form_submission(self):
        response = self.client.post(reverse('rate:register'), {
        'first_name': 'Test',
        'last_name': 'User',
        'username': 'testuser@example.com',
        'password': 'testpass123'
        })

        self.assertEqual(User.objects.count(), 1)
        self.assertRedirects(response, reverse('rate:login'))
