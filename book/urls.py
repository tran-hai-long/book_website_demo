from django.urls import path

from . import views

urlpatterns = [
    path("", views.BookListView.as_view(), name="book_list"),
    path("search/", views.BookSearchView.as_view(), name="book_search"),
    path("book/<int:pk>", views.BookDetailView.as_view(), name="book_detail"),
    path("add-to-cart/<int:pk>", views.add_to_cart, name="add_book_to_cart"),
    path("remove-from-cart/<int:pk>", views.remove_from_cart, name="remove_from_cart"),
    path("shopping-cart/", views.ShoppingCartView.as_view(), name="shopping_cart"),
    path("book/review/<int:pk>", views.review_book, name="review_book"),
]
