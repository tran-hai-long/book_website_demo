from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.test import TestCase
from django.utils import timezone

from book.models import Book, ShoppingCart


class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Book.objects.create(
            title="Django for Beginner",
            author="Tran Hai Long",
            book_description="Test book description.",
            release_date=timezone.now(),
            number_of_pages=999,
            category="Art",
            cover=None,
            price=99.99,
        )

    def setUp(self):
        Book.objects.create(
            title="Django for Beginner Mutable",
            author="Tran Hai Long",
            book_description="Test book description.",
            release_date=timezone.now(),
            number_of_pages=999,
            category="Art",
            cover=None,
            price=99.99,
        )

    def test_title_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field("title").verbose_name
        self.assertEqual(field_label, "title")

    def test_title_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field("title").max_length
        self.assertEqual(max_length, 99)

    def test_author_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field("author").verbose_name
        self.assertEqual(field_label, "author")

    def test_author_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field("author").max_length
        self.assertEqual(max_length, 99)

    def test_book_description_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field("book_description").verbose_name
        self.assertEqual(field_label, "book description")

    def test_book_description_null_blank(self):
        book = Book.objects.get(id=1)
        null_check = book._meta.get_field("book_description").null
        blank_check = book._meta.get_field("book_description").blank
        self.assertEqual(null_check, True)
        self.assertEqual(blank_check, True)

    def test_release_date_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field("release_date").verbose_name
        self.assertEqual(field_label, "release date")

    def test_number_of_pages_date_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field("number_of_pages").verbose_name
        self.assertEqual(field_label, "number of pages")

    def test_number_of_pages_default(self):
        book = Book.objects.get(id=1)
        default_number = book._meta.get_field("number_of_pages").default
        self.assertEqual(default_number, 0)

    def test_category_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field("category").verbose_name
        self.assertEqual(field_label, "category")

    def test_category_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field("category").max_length
        self.assertEqual(max_length, 99)

    def test_category_choices(self):
        book = Book.objects.get(id=1)
        choices = book._meta.get_field("category").choices
        self.assertEqual(choices, book.CATEGORY_CHOICES)

    def test_cover_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field("cover").verbose_name
        self.assertEqual(field_label, "cover")

    def test_cover_null_blank(self):
        book = Book.objects.get(id=1)
        null_check = book._meta.get_field("cover").null
        blank_check = book._meta.get_field("cover").blank
        self.assertEqual(null_check, True)
        self.assertEqual(blank_check, True)

    def test_cover_path(self):
        book = Book.objects.get(id=1)
        path = book._meta.get_field("cover").upload_to
        self.assertEqual(path, "book/%Y/%m/%d/%H%M%S/")

    def test_price_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field("price").verbose_name
        self.assertEqual(field_label, "price")

    def test_price_default(self):
        book = Book.objects.get(id=1)
        default_number = book._meta.get_field("price").default
        self.assertEqual(default_number, 0)

    def test_price_validator(self):
        book = Book.objects.get(id=2)
        book.price = -1
        with self.assertRaises(ValidationError):
            book.clean_fields()

    def test_str_method(self):
        book = Book.objects.get(id=1)
        self.assertEqual(str(book), "Django for Beginner by Tran Hai Long")


class ShoppingCartModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="testuser", email="a@example.com", password="testPassw0rd")
        ShoppingCart.objects.create(user_id=user.pk)

    def test_shopping_cart_user_field(self):
        shopping_cart = ShoppingCart.objects.get(user_id=1)
        self.assertEqual(shopping_cart.user.username, "testuser")

    def test_cascade_on_user_deletion(self):
        user = User.objects.get(id=1)
        user.delete()
        with self.assertRaises(ObjectDoesNotExist):
            ShoppingCart.objects.get(user_id=1)

    def test_str_method(self):
        shopping_cart = ShoppingCart.objects.get(user_id=1)
        self.assertEqual(str(shopping_cart), "Shopping cart of user testuser")
