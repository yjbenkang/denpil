from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Author, Book

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