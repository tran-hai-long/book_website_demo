from django.urls import path

from . import views

app_name = "books"
urlpatterns = [
    path("", views.BookListView.as_view(), name="list"),
    path("search/", views.BookSearchView.as_view(), name="search"),
    path("book/<int:pk>", views.BookDetailView.as_view(), name="detail"),
    path("add-to-cart/<int:pk>", views.add_to_cart, name="add_to_cart"),
    path("remove-from-cart/<int:pk>", views.remove_from_cart, name="remove_from_cart"),
    path("shopping-cart/", views.ShoppingCartView.as_view(), name="shopping_cart"),
    path("book/review/<int:pk>", views.review_book, name="review"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout_page"),
    path("create-invoice/", views.create_invoice, name="create_invoice"),
    path("checkout-complete/", views.CheckoutCompleteView.as_view(), name="checkout_complete"),
    path("invoice-list/", views.InvoiceView.as_view(), name="invoice_list"),
    path("purchased-book-list/<int:pk>", views.PurchasedBookView.as_view(), name="purchased_book_list"),
]
