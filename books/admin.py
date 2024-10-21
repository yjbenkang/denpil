from django.contrib import admin
from .models import Book, Author, BookSalesInfo, PublisherSalesData, BookAgeGenderData, AuthorAgeGenderData
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

@admin.register(BookSalesInfo)
class BookSalesInfoAdmin(admin.ModelAdmin):
    list_display = ('book', 'pricesales', 'pricestandard', 'discount_price', 'discount_rate')
    search_fields = ('book',)

@admin.register(PublisherSalesData)
class PublisherSalesAdmin(admin.ModelAdmin):
    list_display = ('publisher', 'total_sales', 'book_count')
    search_fields = ('publisher',)

@admin.register(BookAgeGenderData)
class BookAgeGenderAdmin(admin.ModelAdmin):
    list_display = ('book', 'age_10', 'age_20', 'age_30', 'age_40', 'age_50', 'age_60', 'male', 'female')
    search_fields = ('book',)

@admin.register(AuthorAgeGenderData)
class AuthorAgeGenderAdmin(admin.ModelAdmin):
    list_display = ('author', 'age_10', 'age_20', 'age_30', 'age_40', 'age_50', 'age_60', 'male', 'female')
    search_fields = ('author',)