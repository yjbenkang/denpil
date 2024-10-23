from django.urls import path
from . import views

urlpatterns = [
    path('', views.author_list, name='book_list'),
    path('author/<int:author_id>/', views.author_books, name='author_books'),
    path('book/<int:book_id>/', views.book_details, name='book_details'),

    # 데이터 마트 관련 url
    path('stat/', views.stat, name='stat'),
    path('stat/book_sales/', views.book_sales_data, name='book_sales'),
    path('stat/publisher/', views.publisher_sales_data, name='publisher_sales'),
    path('stat/book_age/<int:book_id>/', views.book_age_gender_data, name='book_age'),
    path('stat/author_age/<int:author_id>/', views.author_age_gender_data, name='author_age'),
]