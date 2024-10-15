from django.shortcuts import render
from rest_framework import generics
from books.models import Book
from .serializers import BookSerializer

class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all().order_by('-pubdate')  # 최신 순으로 정렬
    serializer_class = BookSerializer
