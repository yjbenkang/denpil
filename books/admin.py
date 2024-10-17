from django.contrib import admin
from .models import Book, Author
from django_apscheduler.models import DjangoJob, DjangoJobExecution


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'nominated_year')
    search_fields = ('name', 'nominated_year', 'description')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pubdate', 'publisher', 'sales_point', 'rating_score', 'rating_count', 'best_duration', 'best_rank')
    search_fields = ('title', 'author')
    list_filter = ('pubdate', 'publisher')
    ordering = ('-pubdate',)
