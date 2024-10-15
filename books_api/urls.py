from django.urls import path
from .views import (
    BookListCreateView, BookDetailView,
    AuthorListCreateView, AuthorDetailView
)

urlpatterns = [
    # Book URLs
    path('books/', BookListCreateView.as_view(), name='book-list-create'),  # List GET, List POST
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),  # Item GET, PUT, PATCH, DELETE

    # Author URLs
    path('authors/', AuthorListCreateView.as_view(), name='author-list-create'),  # List GET, List POST
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),  # Item GET, PUT, PATCH, DELETE
]