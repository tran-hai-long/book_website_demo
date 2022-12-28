from django.contrib import admin

from .models import Book, ShoppingCart, BookInCart, Review

# Register your models here.

admin.site.register(Book)
admin.site.register(ShoppingCart)
admin.site.register(BookInCart)
admin.site.register(Review)
