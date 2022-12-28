from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


# Create your models here.


class Book(models.Model):
    CATEGORY_CHOICES = [
        ("Art", "Arts & Photography"),
        ("Business", "Business & Money"),
        ("Comic", "Comics & Graphic Novels"),
        ("Technology", "Computers & Technology"),
        ("Education", "Education & Teaching"),
        ("Health", "Health, Fitness & Dieting"),
        ("History", "History"),
        ("Literature", "Literature & Fiction"),
        ("Political", "Politics & Social Sciences"),
        ("Science", "Science"),
        ("Sport", "Sports & Outdoors"),
    ]
    title = models.CharField(max_length=99)
    author = models.CharField(max_length=99)
    book_description = models.TextField(null=True, blank=True)
    release_date = models.DateField()
    number_of_pages = models.PositiveSmallIntegerField(default=0)
    category = models.CharField(max_length=99, choices=CATEGORY_CHOICES)
    cover = models.ImageField(upload_to="book/%Y/%m/%d/%H%M%S/", null=True, blank=True)
    price = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    discount = models.SmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f"{self.title} + by + {self.author}"


class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Shopping cart of user {self.user}"


class BookInCart(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.number} copies of book {self.book} in cart {self.cart}."


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(null=True, blank=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"User {self.user.username} rated {self.rating}-star for book {self.book.pk} - {self.book.title}"
