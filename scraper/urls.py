from django.urls import path

from . import views

urlpatterns = [
    path('search/<str:query>/', views.search, name="search"),
    path('search_movie/', views.search_movie, name="search_movie"),
    path('similar/<str:movie_id>/', views.similar, name='similar'),
    path('watch/<str:movie_id>/', views.watch, name='watch'),
    path('play/<str:query>/', views.play, name='play')
]