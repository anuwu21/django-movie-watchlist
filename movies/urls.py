from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('add/', views.add_movie, name='add_movie'),
    path('<int:id>/edit/', views.edit_movie, name='edit_movie'),
    path('<int:id>/delete/', views.delete_movie, name='delete_movie'),
    path('<int:id>/', views.movie_detail, name='movie_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    
]