from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from book.forms import BookSearchForm, ReviewForm, BookNumberForm
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
            context["check_book_in_cart"] = BookInCart.objects.filter(
                cart_id=ShoppingCart.objects.get(user_id=self.request.user.pk), book_id=self.object.pk
            )
        context["book_number_form"] = BookNumberForm()
        context["review_form"] = ReviewForm()
        reviews = Review.objects.filter(book_id=self.object.pk).order_by("date")
        context["reviews"] = reviews
        this_user_review = reviews.filter(user_id=self.request.user.pk)
        context["this_user_review"] = this_user_review
        context["average_rating"] = reviews.aggregate(Avg("rating")).get("rating__avg")
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShoppingCartView, self).get_context_data(**kwargs)
        books_in_cart = BookInCart.objects.filter(cart_id=ShoppingCart.objects.get(user_id=self.request.user.pk))
        total_price = 0
        for book_in_cart in books_in_cart:
            total_price += book_in_cart.book.price * book_in_cart.number
        context["total_price"] = total_price
        return context


@login_required
def add_to_cart(request, pk):
    cart = ShoppingCart.objects.get(user_id=request.user.pk)
    form = BookNumberForm(request.POST)
    if form.is_valid():
        BookInCart(cart_id=cart.pk, book_id=pk, number=form.cleaned_data["number"]).save()
    else:
        return HttpResponse("Error when adding book to cart.")
    return HttpResponseRedirect(reverse("book_detail", args=[pk]))


@login_required
def remove_from_cart(request, pk):
    cart = ShoppingCart.objects.get(user_id=request.user.pk)
    BookInCart.objects.get(cart_id=cart.pk, book_id=pk).delete()
    return HttpResponseRedirect(reverse("shopping_cart"))


@login_required
def review_book(request, pk):
    form = ReviewForm(request.POST)
    if form.is_valid():
        Review.objects.create(
            user_id=request.user.pk,
            book_id=pk,
            rating=form.cleaned_data["rating"],
            comment=form.cleaned_data["comment"],
            date=timezone.now(),
        )
    else:
        return HttpResponse("Error when trying to review this book.")
    return HttpResponseRedirect(reverse("book_detail", args=[pk]))
