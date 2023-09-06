"""
Tests for models.
"""
from django.test import TestCase

from django.contrib.auth import get_user_model

from core import models


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class ModelTests(TestCase):
    """Test models."""

    def test_create_author(self):
        """Test creating a user."""
        user = create_user(
            email='user1@example.com',
            password='testpass123'
        )
        author = models.Author.objects.create(
            user=user,
            first_name='Ivan',
            second_name='Minin'
        )

        self.assertEqual(
            str(author),
            author.first_name + ' ' + author.second_name
        )

    def test_create_genre(self):
        """Test creating a user."""
        user = create_user(
            email='user2@example.com',
            password='testpass123'
        )
        genre = models.Genre.objects.create(
            user=user,
            name='Fantasy'
        )

        self.assertEqual(str(genre), genre.name)

    def test_create_book(self):
        """Test creating a book."""
        user = create_user(
            email='user3@example.com',
            password='testpass123'
        )
        book = models.Book.objects.create(
            user=user,
            title='Harry Potter',
            description='Magical book about magicians',
            total_pages=345,
            published_date='2021-03-23'
        )

        author = models.Author.objects.create(
            user=user,
            first_name='Ivan',
            second_name='Minin'
        )

        genre = models.Genre.objects.create(
            user=user,
            name='Fantasy'
        )

        book.author.add(author)
        book.genres.add(genre)

        self.assertEqual(str(book), book.title)

    def test_create_review(self):
        user = create_user(
            email='user1@example.com',
            password='testpass123'
        )
        book = models.Book.objects.create(
            user=user,
            title='Harry Potter',
            description='Magical book about magicians',
            total_pages=345,
            published_date='2021-03-23'
        )
        author = models.Author.objects.create(
            user=user,
            first_name='Ivan',
            second_name='Minin'
        )

        genre = models.Genre.objects.create(
            user=user,
            name='Fantasy'
        )

        book.author.add(author)
        book.genres.add(genre)

        review = models.Review.objects.create(
            review='I really liked that book, that was so interesting!',
            user=user,
            book=book,
            rating=8,
        )

        self.assertEqual(str(review), review.review)
