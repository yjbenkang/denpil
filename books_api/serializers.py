from rest_framework import serializers
from books.models import Book, Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']
class BookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    class Meta:
        model = Book
        fields = ['title', 'author', 'pubdate', 'description', 'pricesales', 'pricestandard', 'publisher', 'sales_point', 'cover_url', 'link']

    def create(self, validated_data):
        # Book 인스턴스 생성
        author = validated_data.pop('author')  # Author 필드 추출
        book = Book.objects.create(author=author, **validated_data)  # Book 생성
        return book

    def update(self, instance, validated_data):
        # Book 인스턴스 업데이트
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.pubdate = validated_data.get('pubdate', instance.pubdate)
        instance.description = validated_data.get('description', instance.description)
        instance.pricesales = validated_data.get('pricesales', instance.pricesales)
        instance.pricestandard = validated_data.get('pricestandard', instance.pricestandard)
        instance.publisher = validated_data.get('publisher', instance.publisher)
        instance.sales_point = validated_data.get('sales_point', instance.sales_point)
        instance.cover_url = validated_data.get('cover_url', instance.cover_url)
        instance.link = validated_data.get('link', instance.link)
        instance.save()
        return instance