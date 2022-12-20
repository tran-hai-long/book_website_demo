from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from book.forms import BookSearchForm
from book.models import Book, ShoppingCart, BookInCart


class BookListView(ListView):
    model = Book
    paginate_by = 20
    search_form = BookSearchForm()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context["form"] = self.search_form
        return context


class BookDetailView(DetailView):
    model = Book

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context["books_in_cart"] = BookInCart.objects.all()
        return context


class BookSearchView(ListView):
    model = Book
    paginate_by = 20

    def get_queryset(self):
        form = BookSearchForm(self.request.GET)
        if form.is_valid():
            search_term = form.cleaned_data["title"]
            return super().get_queryset().filter(title__icontains=search_term)


def add_to_cart(request, pk):
    cart = ShoppingCart.objects.get(user_id=request.user.pk)
    book = Book.objects.get(pk=pk)
    BookInCart(cart_id=cart.pk, book_id=book.pk).save()
    return redirect("/books/")
