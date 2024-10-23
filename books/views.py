from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import BookSalesSerializer, PublisherSerializer

def author_list(request):
    authors = Author.objects.all().order_by('-nominated_year')
    return render(request, 'books/book_list.html', {'authors': authors})
def author_books(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    author_dict = {
        'id': author.id,
        'name': author.name,
        'image': author.image,
        'nominated_year': author.nominated_year,
        'description': author.description
    }
    books = Book.objects.filter(author=author)
    book_list = [{
        'id': book.id,
        'title': book.title,
        'cover_url': book.cover_url,
        'rating_score': book.rating_score,
        'pricesales': book.pricesales,
        'pricestandard': book.pricestandard,
        'rating_count': book.rating_count,
        'best_duration': book.best_duration,
        'best_rank': book.best_rank,
        'publisher': book.publisher,
        'sales_point': book.sales_point,
        'age_gender_ratings': book.age_gender_ratings,
        } for book in books]
    return JsonResponse({'author': author_dict, 'books': book_list})

def book_details(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    data = {
        'title': book.title,
        'author': book.author.name,
        'pubdate': book.pubdate,
        'description': book.description,
        'pricesales': book.pricesales,
        'pricestandard': book.pricestandard,
        'rating_score': book.rating_score,
        'rating_count': book.rating_count,
        'best_duration': book.best_duration,
        'best_rank': book.best_rank,
        'publisher': book.publisher,
        'sales_point': book.sales_point,
        'cover_url': book.cover_url,
        'link': book.link,
        'age_gender_ratings': book.age_gender_ratings,

    }
    return JsonResponse(data)

# 여기서 부터 통계
def stat(request):
    books = Book.objects.all()
    authors = Author.objects.all()
    return render(request, 'books/stat.html', {'books':books, 'authors':authors})

@api_view(['GET'])
def book_sales_data(request):
    book_sales = BookSalesInfo.objects.all()
    serializer = BookSalesSerializer(book_sales, many=True)
    return Response(serializer.data)

# 2. 출판사별 판매량 및 책 개수
@api_view(['GET'])
def publisher_sales_data(request):
    pub_sales = PublisherSalesData.objects.all()
    serializer = PublisherSerializer(pub_sales, many=True)
    return Response(serializer.data)

# 3. 책별 연령 및 성별 데이터
def book_age_gender_data(request, book_id):
    book_age = get_object_or_404(BookAgeGenderData, book__id=book_id)
    data = {
        'age_10': book_age.age_10,
        'age_20': book_age.age_20,
        'age_30': book_age.age_30,
        'age_40': book_age.age_40,
        'age_50': book_age.age_50,
        'age_60': book_age.age_60,
        'male': book_age.male,
        'female': book_age.female,
    }
    return JsonResponse(data)

# 4. 작가별 연령 및 성별 데이터
def author_age_gender_data(request, author_id):
    author_age = get_object_or_404(AuthorAgeGenderData, author__id=author_id)
    data = {
        'age_10': author_age.age_10,
        'age_20': author_age.age_20,
        'age_30': author_age.age_30,
        'age_40': author_age.age_40,
        'age_50': author_age.age_50,
        'age_60': author_age.age_60,
        'male': author_age.male,
        'female': author_age.female,
    }
    return JsonResponse(data)