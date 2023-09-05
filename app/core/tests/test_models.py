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
