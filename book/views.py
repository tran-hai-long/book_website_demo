from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from book.forms import BookSearchForm, ReviewForm, BookNumberForm, CheckoutForm
from book.models import Book, ShoppingCart, BookInCart, Review, Invoice, PurchasedBook


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


@method_decorator(login_required, name="dispatch")
class InvoiceView(ListView):
    model = Invoice
    ordering = ["-date"]

    def get_queryset(self):
        return super().get_queryset().filter(user_id=self.request.user.pk)


@method_decorator(login_required, name="dispatch")
class PurchasedBookView(ListView):
    model = PurchasedBook

    def get_queryset(self):
        invoice_id = self.kwargs["pk"]
        invoice = Invoice.objects.get(pk=invoice_id)
        if invoice.user_id == self.request.user.pk:
            return super().get_queryset().filter(invoice_id=invoice_id)
        else:
            return super().get_queryset().none()


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


@method_decorator(login_required, name="dispatch")
class CheckoutView(ListView):
    model = BookInCart
    template_name = "book/checkout.html"

    def get_queryset(self):
        return super().get_queryset().filter(cart_id=ShoppingCart.objects.get(user_id=self.request.user.pk))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        context["form"] = CheckoutForm()
        books_in_cart = BookInCart.objects.filter(cart_id=ShoppingCart.objects.get(user_id=self.request.user.pk))
        total_price = 0
        for book_in_cart in books_in_cart:
            total_price += book_in_cart.book.price * book_in_cart.number
        context["total_price"] = total_price
        return context


@login_required
def create_invoice(request):
    form = CheckoutForm(request.POST)
    if form.is_valid():
        books_in_cart = BookInCart.objects.filter(cart_id=ShoppingCart.objects.get(user_id=request.user.pk))
        total_price = 0
        for book_in_cart in books_in_cart:
            total_price += book_in_cart.book.price * book_in_cart.number
        invoice = Invoice.objects.create(
            user_id=request.user.pk,
            shipping_address=form.cleaned_data["shipping_address"],
            phone_number=form.cleaned_data["phone_number"],
            payment_method=form.cleaned_data["payment_method"],
            date=timezone.now(),
            total_price=total_price,
        )
        for book_in_cart in books_in_cart:
            PurchasedBook.objects.create(
                invoice_id=invoice.pk, book_id=book_in_cart.book.pk, number=book_in_cart.number
            )
            book_in_cart.delete()
        return HttpResponseRedirect(reverse("checkout_complete"))
    else:
        return HttpResponse("Error processing transaction.")


def checkout_complete(request):
    return render(request, "book/checkout_complete.html")
