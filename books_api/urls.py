from django.urls import path
from .views import BookListAPIView

urlpatterns = [
    path('books/', BookListAPIView.as_view(), name='book_list_api'),
]