from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Author, Book

def author_list(request):
    authors = Author.objects.all()
    return render(request, 'books/book_list.html', {'authors': authors})

def author_books(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    books = Book.objects.filter(author=author)
    book_list = [{'id': book.id, 'title': book.title} for book in books]
    return JsonResponse({'author': author.name, 'books': book_list})

def book_details(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    data = {
        'title': book.title,
        'description': book.description,
    }
    return JsonResponse(data)