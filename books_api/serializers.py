from rest_framework import serializers
from books.models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'pubdate', 'description', 'pricesales', 'pricestandard', 'publisher', 'sales_point', 'cover_url', 'link']