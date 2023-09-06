"""
Tests for genre model.
"""
from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from core.models import Genre
from genres.serializers import GenreSerializer

GENRES_URL = reverse('genre:genre-list')


def detail_url(genre_id):
    return reverse('genre:genre-detail', args=[genre_id])


def create_genre(user, **params):
    defaults = {
        'name': 'Romance'
    }

    defaults.update(params)

    genre = Genre.objects.create(user=user, **defaults)

    return genre


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PrivateGenreAPITests(TestCase):
    """Test genres API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='alex5@exa.com',
            password='testpassword123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_genres(self):
        create_genre(user=self.user)

        res = self.client.get(GENRES_URL)

        genres = Genre.objects.all().order_by('-id')
        serializer = GenreSerializer(genres, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_genre(self):
        """Test updating a genre."""
        genre = Genre.objects.create(user=self.user, name="Horrific")
        payload = {'name': 'Reality'}

        url = detail_url(genre.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        genre.refresh_from_db()
        self.assertEqual(genre.name, payload['name'])

    def test_delete_genre(self):
        """Test deleting a genre."""
        genre = Genre.objects.create(user=self.user, name='Historical')

        url = detail_url(genre.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Genre.objects.filter(id=genre.id).exists())
