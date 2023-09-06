"""
Tests for author model.
"""
from django.test import TestCase

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


class PrivateAuthorAPITests(TestCase):
    """Test authors API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_authors(self):
        create_author(user=self.user)

        res = self.client.get(AUTHORS_URL)

        authors = Author.objects.all().order_by('-id')
        serializer = AuthorSerializer(authors, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_author(self):
        """Test updating an author."""
        author = Author.objects.create(
            user=self.user,
            first_name='Antony',
            second_name='Kireev',
        )
        payload = {'first_name': 'Alexander'}

        url = detail_url(author.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        author.refresh_from_db()
        self.assertEqual(author.first_name, payload['first_name'])

    def test_delete_authors(self):
        """Test deleting a genre."""
        author = Author.objects.create(
            user=self.user,
            first_name='Igor',
            second_name='Venskiy',
        )

        url = detail_url(author.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Author.objects.filter(id=author.id).exists())
