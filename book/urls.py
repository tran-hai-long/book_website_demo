from django.urls import path

from . import views

urlpatterns = [
    path("", views.BookListView.as_view(), name="book_list"),
    path("book/<int:pk>", views.BookDetailView.as_view(), name="book_detail"),
    path("book/add-to-cart/<int:pk>", views.add_to_cart, name="add_book_to_cart"),
    path("search/", views.BookSearchView.as_view(), name="book_search"),
]
