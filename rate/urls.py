from django.urls import path
from rate import views

app_name = 'rate'

urlpatterns = [
    path('', views.index, name='index'),
    path('genres/', views.genres, name='genres'),
    path('add_rating/', views.add_rating, name ='add_rating'),
    path('my_media/', views.my_media, name='my_media'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
]