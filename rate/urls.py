from django.urls import path, reverse_lazy
from rate import views
from django.contrib.auth import views as auth_views

app_name = 'rate'

urlpatterns = [
    path('', views.index, name='index'),
    path('genres/', views.genres, name='genres'),
    path('add_rating/', views.add_rating, name ='add_rating'),
    path('my_media/', views.my_media, name='my_media'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('rate:index')), name='auth_password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]