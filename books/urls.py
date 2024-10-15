from . import views
from django.urls import path

urlpatterns = [
    path("", views.book_list, name="book_list"),
]