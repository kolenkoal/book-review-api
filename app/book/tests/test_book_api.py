"""
Tests for book model.
"""
from book.serializers import BookSerializer
from core import models
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


BOOKS_URL = reverse("book:book-list")


def detail_url(book_id):
    return reverse("book:book-detail", args=[book_id])


def create_book(user, **params):
    defaults = {
        "title": "Harry Potter",
        "description": "Magical book about magicians",
        "total_pages": 345,
        "published_date": "2021-03-23",
    }

    defaults.update(params)

    book = models.Book.objects.create(user=user, **defaults)

    return book


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PrivateBookAPITests(TestCase):
    """Test books API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email="alex6@exa.com", password="testpassword123"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_books(self):
        create_book(user=self.user)
        create_book(user=self.user)

        res = self.client.get(BOOKS_URL)

        books = models.Book.objects.all().order_by("-id")
        serializer = BookSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_book_detail(self):
        """Test get book detail."""
        book = create_book(user=self.user)

        url = detail_url(book.id)
        res = self.client.get(url)

        serializer = BookSerializer(book)

        self.assertEqual(res.data, serializer.data)

    def test_update_book(self):
        """Test updating a book."""
        book = create_book(user=self.user)
        payload = {"title": "Reality"}

        url = detail_url(book.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.title, payload["title"])

    def test_delete_book(self):
        """Test deleting a book."""
        book = create_book(user=self.user)

        url = detail_url(book.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Book.objects.filter(id=book.id).exists())

    def test_update_user_returns_error(self):
        """Test changing the book user results in an error."""
        new_user = create_user(email="user5@example.com", password="test123")
        recipe = create_book(user=self.user)

        payload = {"user": new_user.id}
        url = detail_url(recipe.id)

        self.client.patch(url, payload)
        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)

    def test_create_book_with_new_author(self):
        defaults = {
            "title": "Fantasy",
            "description": "Magic is here",
            "total_pages": 308,
            "published_date": "2009-09-04",
            "author": [{"first_name": "Arkadiy", "second_name": "Volhov"}],
            "genres": [{"name": "Cinematic"}],
        }

        res = self.client.post(BOOKS_URL, defaults, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        books = models.Book.objects.filter(user=self.user)
        self.assertEqual(books.count(), 1)
        book = books[0]
        self.assertEqual(book.author.count(), 1)
        for author in defaults["author"]:
            exists = book.author.filter(
                first_name=author["first_name"],
                second_name=author["second_name"],
                user=self.user,
            ).exists()
            self.assertTrue(exists)

    def test_create_book_with_existing_genres(self):
        """Test creating a book with exiting genres."""
        genre_space = models.Genre.objects.create(user=self.user, name="Space")
        payload = {
            "title": "Pongal",
            "description": "Magic!",
            "total_pages": 200,
            "published_date": "2010-01-01",
            "author": [{"first_name": "Arkadiy", "second_name": "Volhov"}],
            "genres": [{"name": "Cinematic"}, {"name": "Space"}],
        }
        res = self.client.post(BOOKS_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        books = models.Book.objects.filter(user=self.user)
        self.assertEqual(books.count(), 1)
        book = books[0]
        self.assertEqual(book.genres.count(), 2)
        self.assertIn(genre_space, book.genres.all())
        for genre in payload["genres"]:
            exists = book.genres.filter(
                name=genre["name"],
                user=self.user,
            ).exists()
            self.assertTrue(exists)

    def test_create_genre_on_update(self):
        """Test creating genre when updating a book."""
        book = create_book(user=self.user)
        payload = {"genres": [{"name": "Historic"}]}
        url = detail_url(book.id)
        res = self.client.patch(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_genre = models.Genre.objects.get(user=self.user, name="Historic")
        self.assertIn(new_genre, book.genres.all())

    def test_update_book_assign_genres(self):
        """Test assigning an existing genre when updating a book."""
        genre_melodrama = models.Genre.objects.create(
            user=self.user, name="Melodrama"
        )
        book = create_book(user=self.user)
        book.genres.add(genre_melodrama)

        genre_grass = models.Genre.objects.create(user=self.user, name="Grass")
        payload = {"genres": [{"name": "Grass"}]}

        url = detail_url(book.id)
        res = self.client.patch(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(genre_grass, book.genres.all())
        self.assertNotIn(genre_melodrama, book.genres.all())

    def test_clear_recipe_tags(self):
        """Test clearing a recipes tags"""
        genre = models.Genre.objects.create(user=self.user, name="Reality")
        book = create_book(user=self.user)
        book.genres.add(genre)

        payload = {"genres": []}

        url = detail_url(book.id)
        res = self.client.patch(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn(genre, book.genres.all())
        self.assertEqual(book.genres.all().count(), 0)
