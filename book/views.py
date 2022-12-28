from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from book.forms import BookSearchForm, ReviewForm
from book.models import Book, ShoppingCart, BookInCart, Review


class BookListView(ListView):
    model = Book
    paginate_by = 20
    search_form = BookSearchForm()
    ordering = ["title", "author", "release_date"]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context["form"] = self.search_form
        return context


class BookDetailView(DetailView):
    model = Book

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["books_in_cart"] = BookInCart.objects.filter(
                cart_id=ShoppingCart.objects.get(user_id=self.request.user.pk), book_id=self.object.pk
            )
        context["review_form"] = ReviewForm()
        context["reviews"] = Review.objects.filter(book_id=self.object.pk)
        return context


class BookSearchView(ListView):
    model = Book
    paginate_by = 20
    search_form = BookSearchForm()
    ordering = ["title", "author", "release_date"]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookSearchView, self).get_context_data(**kwargs)
        context["form"] = self.search_form
        return context

    def get_queryset(self):
        form = BookSearchForm(self.request.GET)
        if form.is_valid():
            search_term = form.cleaned_data["title"]
            return super().get_queryset().filter(title__icontains=search_term)


@method_decorator(login_required, name="dispatch")
class ShoppingCartView(ListView):
    model = BookInCart
    template_name = "book/shopping_cart.html"

    def get_queryset(self):
        return super().get_queryset().filter(cart_id=ShoppingCart.objects.get(user_id=self.request.user.pk))


@login_required
def add_to_cart(request, pk):
    cart = ShoppingCart.objects.get(user_id=request.user.pk)
    BookInCart(cart_id=cart.pk, book_id=pk).save()
    return HttpResponseRedirect(reverse("book_detail", args=[pk]))


@login_required
def remove_from_cart(request, pk):
    cart = ShoppingCart.objects.get(user_id=request.user.pk)
    BookInCart.objects.get(cart_id=cart.pk, book_id=pk).delete()
    return HttpResponseRedirect(reverse("shopping_cart"))


def review_book(request, pk):
    form = ReviewForm(request.POST)
    if form.is_valid():
        Review.objects.create(
            user_id=request.user.pk,
            book_id=pk,
            rating=form.cleaned_data["rating"],
            comment=form.cleaned_data["comment"],
            date=timezone.now,
        )
    else:
        return HttpResponse("Error when trying to review this book.")
    return HttpResponseRedirect(reverse("book_detail", args=[pk]))
