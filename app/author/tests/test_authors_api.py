"""
Tests for author model.
"""
from unittest import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from author.serializers import AuthorSerializer
from core.models import Author

AUTHORS_URL = reverse('authors:authors-list')


def detail_url(author_id):
    return reverse('authors:authors-detail', args=[author_id])


def create_author(user, **params):
    defaults = {
        'first_name': 'Mikhail',
        'second_name': 'Loshak',
    }

    defaults.update(params)

    author = Author.objects.create(user=user, **defaults)

    return author


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicAuthorAPITests(TestCase):
    """Test authors API."""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_recipes(self):
        res = self.client.get(AUTHORS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAuthorAPITests(TestCase):
    """Test authors API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        create_author(user=self.user)

        res = self.client.get(AUTHORS_URL)

        authors = Author.objects.all().order_by('-id')
        serializer = AuthorSerializer(authors, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
