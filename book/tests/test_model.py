from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.test import TestCase
from django.utils import timezone

from book.models import Book, ShoppingCart, BookInCart, Review


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
        book = Book.objects.get(pk=1)
        field_label = book._meta.get_field("title").verbose_name
        self.assertEqual(field_label, "title")

    def test_title_max_length(self):
        book = Book.objects.get(pk=1)
        max_length = book._meta.get_field("title").max_length
        self.assertEqual(max_length, 99)

    def test_author_label(self):
        book = Book.objects.get(pk=1)
        field_label = book._meta.get_field("author").verbose_name
        self.assertEqual(field_label, "author")

    def test_author_max_length(self):
        book = Book.objects.get(pk=1)
        max_length = book._meta.get_field("author").max_length
        self.assertEqual(max_length, 99)

    def test_book_description_label(self):
        book = Book.objects.get(pk=1)
        field_label = book._meta.get_field("book_description").verbose_name
        self.assertEqual(field_label, "book description")

    def test_book_description_null_blank(self):
        book = Book.objects.get(pk=1)
        null_check = book._meta.get_field("book_description").null
        blank_check = book._meta.get_field("book_description").blank
        self.assertEqual(null_check, True)
        self.assertEqual(blank_check, True)
        book.book_description = None
        book.clean_fields()

    def test_release_date_label(self):
        book = Book.objects.get(pk=1)
        field_label = book._meta.get_field("release_date").verbose_name
        self.assertEqual(field_label, "release date")

    def test_number_of_pages_date_label(self):
        book = Book.objects.get(pk=1)
        field_label = book._meta.get_field("number_of_pages").verbose_name
        self.assertEqual(field_label, "number of pages")

    def test_number_of_pages_default(self):
        book = Book.objects.get(pk=1)
        default_number = book._meta.get_field("number_of_pages").default
        self.assertEqual(default_number, 0)

    def test_category_label(self):
        book = Book.objects.get(pk=1)
        field_label = book._meta.get_field("category").verbose_name
        self.assertEqual(field_label, "category")

    def test_category_max_length(self):
        book = Book.objects.get(pk=1)
        max_length = book._meta.get_field("category").max_length
        self.assertEqual(max_length, 99)

    def test_category_choices(self):
        book = Book.objects.get(pk=1)
        choices = book._meta.get_field("category").choices
        self.assertEqual(choices, book.CATEGORY_CHOICES)

    def test_cover_label(self):
        book = Book.objects.get(pk=1)
        field_label = book._meta.get_field("cover").verbose_name
        self.assertEqual(field_label, "cover")

    def test_cover_null_blank(self):
        book = Book.objects.get(pk=1)
        null_check = book._meta.get_field("cover").null
        blank_check = book._meta.get_field("cover").blank
        self.assertEqual(null_check, True)
        self.assertEqual(blank_check, True)

    def test_cover_path(self):
        book = Book.objects.get(pk=1)
        path = book._meta.get_field("cover").upload_to
        self.assertEqual(path, "book/%Y/%m/%d/%H%M%S/")

    def test_price_label(self):
        book = Book.objects.get(pk=1)
        field_label = book._meta.get_field("price").verbose_name
        self.assertEqual(field_label, "price")

    def test_price_default(self):
        book = Book.objects.get(pk=1)
        default_number = book._meta.get_field("price").default
        self.assertEqual(default_number, 0)

    def test_price_validator(self):
        book = Book.objects.get(id=2)
        book.price = -1
        with self.assertRaises(ValidationError):
            book.clean_fields()

    def test_str_method(self):
        book = Book.objects.get(pk=1)
        self.assertEqual(str(book), "Django for Beginner by Tran Hai Long")


class ShoppingCartModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="testuser", email="a@example.com", password="testPassw0rd")
        ShoppingCart.objects.create(user_id=user.pk)

    def test_shopping_cart_user_reference(self):
        shopping_cart = ShoppingCart.objects.get(user_id=1)
        self.assertEqual(shopping_cart.user.username, "testuser")

    def test_user_label(self):
        shopping_cart = ShoppingCart.objects.get(user_id=1)
        user = shopping_cart._meta.get_field("user").verbose_name
        self.assertEqual(user, "user")

    def test_cascade_on_user_deletion(self):
        user = User.objects.get(pk=1)
        user.delete()
        with self.assertRaises(ObjectDoesNotExist):
            ShoppingCart.objects.get(user_id=1)

    def test_str_method(self):
        shopping_cart = ShoppingCart.objects.get(user_id=1)
        self.assertEqual(str(shopping_cart), "Shopping cart of user testuser")


class BookInCartModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        book = Book.objects.create(
            title="Django for Beginner",
            author="Tran Hai Long",
            book_description="Test book description.",
            release_date=timezone.now(),
            number_of_pages=999,
            category="Art",
            cover=None,
            price=99.99,
        )
        user = User.objects.create_user(username="testuser", email="a@example.com", password="testPassw0rd")
        cart = ShoppingCart.objects.create(user_id=user.pk)
        BookInCart.objects.create(cart_id=cart.pk, book_id=book.pk)

    def test_cart_label(self):
        book_in_cart = BookInCart.objects.get(pk=1)
        cart = book_in_cart._meta.get_field("cart").verbose_name
        self.assertEqual(cart, "cart")

    def test_book_label(self):
        book_in_cart = BookInCart.objects.get(pk=1)
        book = book_in_cart._meta.get_field("book").verbose_name
        self.assertEqual(book, "book")

    def test_number_label(self):
        book_in_cart = BookInCart.objects.get(pk=1)
        number = book_in_cart._meta.get_field("number").verbose_name
        self.assertEqual(number, "number")

    def test_cart_reference(self):
        book_in_cart = BookInCart.objects.get(pk=1)
        self.assertEqual(book_in_cart.cart.user.username, "testuser")

    def test_book_reference(self):
        book_in_cart = BookInCart.objects.get(pk=1)
        self.assertEqual(book_in_cart.book.title, "Django for Beginner")

    def test_cart_cascade(self):
        cart = ShoppingCart.objects.get(pk=1)
        cart.delete()
        with self.assertRaises(ObjectDoesNotExist):
            BookInCart.objects.get(pk=1)

    def test_book_cascade(self):
        book = Book.objects.get(pk=1)
        book.delete()
        with self.assertRaises(ObjectDoesNotExist):
            BookInCart.objects.get(pk=1)

    def test_number_default(self):
        book_in_cart = BookInCart.objects.get(pk=1)
        default_number = book_in_cart._meta.get_field("number").default
        self.assertEqual(default_number, 1)

    def test_number_validator(self):
        book_in_cart = BookInCart.objects.get(pk=1)
        book_in_cart.number = 0
        with self.assertRaises(ValidationError):
            book_in_cart.clean_fields()

    def test_str_method(self):
        book_in_cart = BookInCart.objects.get(pk=1)
        self.assertEqual(str(book_in_cart), "1 copies of book 1 - Django for Beginner in cart testuser.")


class ReviewModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        book = Book.objects.create(
            title="Django for Beginner",
            author="Tran Hai Long",
            book_description="Test book description.",
            release_date=timezone.now(),
            number_of_pages=999,
            category="Art",
            cover=None,
            price=99.99,
        )
        user = User.objects.create_user(username="testuser", email="a@example.com", password="testPassw0rd")
        Review.objects.create(user_id=user.pk, book_id=book.pk, rating=1)

    def test_user_label(self):
        review = Review.objects.get(pk=1)
        self.assertEqual(review._meta.get_field("user").verbose_name, "user")

    def test_book_label(self):
        review = Review.objects.get(pk=1)
        self.assertEqual(review._meta.get_field("book").verbose_name, "book")

    def test_rating_label(self):
        review = Review.objects.get(pk=1)
        self.assertEqual(review._meta.get_field("rating").verbose_name, "rating")

    def test_comment_label(self):
        review = Review.objects.get(pk=1)
        self.assertEqual(review._meta.get_field("comment").verbose_name, "comment")

    def test_date_label(self):
        review = Review.objects.get(pk=1)
        self.assertEqual(review._meta.get_field("date").verbose_name, "date")

    def test_user_reference(self):
        review = Review.objects.get(pk=1)
        self.assertEqual(review.user.username, "testuser")

    def test_book_reference(self):
        review = Review.objects.get(pk=1)
        self.assertEqual(review.book.title, "Django for Beginner")

    def test_user_null_on_deletion(self):
        user = User.objects.get(pk=1)
        user.delete()
        review = Review.objects.get(pk=1)
        self.assertIsNone(review.user)

    def test_book_cascade(self):
        book = Book.objects.get(pk=1)
        book.delete()
        with self.assertRaises(ObjectDoesNotExist):
            Review.objects.get(pk=1)

    def test_rating_default(self):
        review = Review.objects.get(pk=1)
        default_rating = review._meta.get_field("rating").default
        self.assertEqual(default_rating, 3)

    def test_rating_validation(self):
        review = Review.objects.get(pk=1)
        review.rating = 0
        with self.assertRaises(ValidationError):
            review.clean_fields()
        review.rating = 6
        with self.assertRaises(ValidationError):
            review.clean_fields()

    def test_comment_null_blank(self):
        review = Review.objects.get(pk=1)
        null_check = review._meta.get_field("comment").null
        blank_check = review._meta.get_field("comment").blank
        self.assertEqual(null_check, True)
        self.assertEqual(blank_check, True)
        review.comment = None
        review.clean_fields()

    def test_str_method(self):
        review = Review.objects.get(pk=1)
        self.assertEqual(str(review), "User testuser rated 1-star for book 1 - Django for Beginner.")
        user = User.objects.get(pk=1)
        user.delete()
        review = Review.objects.get(pk=1)
        self.assertEqual(str(review), "A deleted user rated 1-star for book 1 - Django for Beginner.")
