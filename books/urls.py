from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('<int:circle_id>/select/<str:google_books_id>/', views.select_book, name='select_book'),
    path('<int:circle_id>/finish/', views.finish_book, name='finish_book'),
    path('<int:circle_id>/books/discover', views.search_books_for_voting, name='search_books_for_voting'),
    path('<int:circle_id>/books/vote/<str:google_books_id>/', views.vote_for_book, name='vote_for_book'),
]