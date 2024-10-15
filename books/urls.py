from django.urls import path
from . import views

urlpatterns = [
    path('', views.author_list, name='book_list'),
    path('author/<int:author_id>/', views.author_books, name='author_books'),
    path('book/<int:book_id>/', views.book_details, name='book_details'),
]